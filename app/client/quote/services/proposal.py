from app.client.quote.services.crud import get_quote
from flask import request

from app.admin.user.services.crud import get_user
from app.auth.services.user import get_user_jwt
from app.client.quote.models import Quote, QuoteProposal
from app.client.quote.schemas import QuoteProposalSchema
from app.client.quote.services.notification_to_users import send_proposal_accepted_email, send_to_client_email
from app.client.quote.services.proposal_products import create_proposal_products, update_proposal_products, \
    gets_proposal_product
from app.services.api_server.requests import custom_filters
from app.services.errors.exceptions import GenerateError, NotFoundError


def create_quote_proposal(id, schema=False):
    user_jwt = get_user_jwt()
    user = get_user(user_jwt["user_id"])

    if user.receive_quotes is True:
        dict_body = request.get_json()

        quote = Quote.query.filter(Quote.id == id, Quote.deleted_at == None).first()

        if quote:
            dict_body["quote_id"] = id
            dict_body["company_id"] = user.company_id
            item = QuoteProposal().create_item(dict_body).save()

            if 'products' in dict_body:
                create_proposal_products(item, dict_body["products"])
        else:
            raise NotFoundError()

        item = get_quote_proposal(item.id, schema)
        if item:
            send_to_client_email(quote, item)
    else:
        raise PermissionError()

    return item


def get_quote_proposal(id, schema=None, columns=None):
    query = QuoteProposal.query
    if columns:
        query = query.with_entities(*[getattr(QuoteProposal, column) for column in columns])
    item = query.filter(QuoteProposal.id == id).first()
    if not item:
        raise NotFoundError()
    if schema:
        item = QuoteProposalSchema().dump(item)
    return item


def gets_quote_proposal(id, schema=None, columns=None):
    dict_filters = custom_filters()
    query = QuoteProposal.query.filter(QuoteProposal.quote_id == id, QuoteProposal.deleted_at == None)
    if columns:
        query = query.with_entities(*[getattr(QuoteProposal, column) for column in columns])
        
        
    if dict_filters["created_at_start"] or dict_filters["created_at_end"]:
        query = query.filter(QuoteProposal.created_at.between(dict_filters["created_at_start"], 
                                                      dict_filters["created_at_end"]))
        
    if dict_filters["order_by_column"] == "price":
        query = query.order_by(QuoteProposal.price.asc())
    items = query.paginate(dict_filters["page"], dict_filters["per_page"], False)
    items_paginate = items
    if schema:
        items = QuoteProposalSchema(many=True).dump(items.items)

    return items, items_paginate


def update_quote_proposal(id, schema=None):
    item = get_quote_proposal(id)

    dict_body = request.get_json()
    if item.status == 2:
        raise GenerateError("Cotação concluída!", 400)

    item.update_item(dict_body).update()

    if "products" in dict_body:
        update_proposal_products(item, dict_body["products"])
    if item.status == 2:
        quote = get_quote(item.quote_id, True)
        send_proposal_accepted_email(quote, item.company_id)

    if schema:
        item = QuoteProposalSchema().dump(item)
    return item


def delete_quote_proposal(id):
    item = get_quote_proposal(id)
    if item:
        item.delete()
        products = gets_proposal_product(id)
        for product in products:
            product.delete()
    else:
        raise NotFoundError()
    return True
