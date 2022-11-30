from app.admin.user.models import User
from app.services.utils.utils import get_now
from flask import request
from sqlalchemy import or_, and_

from app.admin.notification.models import NotificationSend, Notification
from app.auth.services.user import get_user_jwt
from app.client.quote.models import Quote, QuoteAddress, QuoteProposal
from app.client.quote.schemas import QuoteSchema
from app.client.quote.services.notification_to_users import send_to_providers_email_notification
from app.client.quote.services.products import create_quote_products, update_quote_products
from app.client.quote.services.submitted_proposal import verify_proposal
from app.services.api_server.requests import custom_filters
from app.services.errors.exceptions import NotFoundError


def gets_quote(schema=None, columns=None, user=None):
    dict_filters = custom_filters()
    dict_filters["status"] = request.args.get("status", type=int)
    dict_filters["segment"] = tuple(request.args.getlist('segment[]'))
    query = Quote.query.filter(Quote.deleted_at == None)
    user = User.get_by_id(user["user_id"])
    if columns:
        query = query.with_entities(*[getattr(Quote, column) for column in columns])
    if dict_filters["search"]:
        query = query.filter(
            or_(Quote.name.like(f'%%{dict_filters["search"]}%%')))
    if dict_filters["status"] is not None:
        query = query.filter(Quote.status == dict_filters["status"])
    else:
        query = query.filter(Quote.status > 0)

    if dict_filters["segment"]:
        query = query.filter(Quote.segment_id.in_(dict_filters["segment"]))
        
    if dict_filters["created_at_start"] or dict_filters["created_at_end"]:
        query = query.filter(Quote.created_at.between(dict_filters["created_at_start"], 
                                                      dict_filters["created_at_end"]))
        
    if user:
        if user.group_id == 5 or dict_filters["status"] == 0:
            query = query.filter(Quote.user_id == user.id)
        if user.group_id == 4:
            query = query.outerjoin(QuoteProposal, QuoteProposal.quote_id == Quote.id)\
                .filter(or_(and_(Quote.proposals_deadline >= get_now(), Quote.status != 2), 
                            QuoteProposal.company_id == user.company_id))
        
    items = query.order_by(Quote.id.desc()).paginate(
        dict_filters["page"], dict_filters["per_page"], False)
    
    items_paginate = items
    if schema:
        items = QuoteSchema(many=True).dump(items.items)
        for item in items:
            item["proposal_sent"] = verify_proposal(item)

    return items, items_paginate


def get_quote(id, schema=None, columns=None):
    query = Quote.query
    if columns:
        query = query.with_entities(*[getattr(Quote, column) for column in columns])
    item = query.filter(Quote.id == id).first()

    if not item:
        raise NotFoundError()
    if schema:
        item = QuoteSchema().dump(item)
        item["proposal_sent"] = verify_proposal(item)
    return item


def create_quote(schema=None):
    dict_body = request.get_json()
    dict_body["user_id"] = get_user_jwt()["user_id"]

    item = Quote().create_item(dict_body).save()

    if 'address' in dict_body:
        dict_body['address']['quote_id'] = item.id
        QuoteAddress().create_item(dict_body["address"]).save()

    if "products" in dict_body:
        create_quote_products(item, dict_body["products"])

    item = get_quote(item.id, schema)

    # SEND EMAILS AND NOTIFICATIONS
    if item["status"] != 0:
        send_to_providers_email_notification(item)

    return item


def update_quote(id, schema=None):
    item = get_quote(id)
    dict_body = request.get_json()

    if item.status > 0:
        if dict_body["status"] != item.status:
            item.status = dict_body["status"]
            item.update()
            if item.status == 2:
                notification = Notification.query \
                    .filter(Notification.quote_id == id).first()
                notification_send = NotificationSend.query \
                    .filter(NotificationSend.notification_id == notification.id) \
                    .all()
                notification.name = "Cotação Concluída!"
                notification.update()
                for item in notification_send:
                    item.name = "Cotação Concluída!"
                    item.update()
        else:
            raise NotFoundError("Cotação já enviada")

    item.update_item(dict_body).update()

    # update products of quote
    if "products" in dict_body:
        update_quote_products(item.id, dict_body["products"])

    if schema:
        item = QuoteSchema().dump(item)
        # SEND EMAILS AND NOTIFICATIONS
        if item["status"] != 0:
            send_to_providers_email_notification(item)
            
    return item


def delete_quote(id):
    item = get_quote(id)
    item.delete()
    return True
