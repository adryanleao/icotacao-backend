from flask import request

from app.admin.notification.models import Notification, NotificationSend
from app.admin.notification.schemas import NotificationSchema
from app.admin.notification.services.notification_quote import get_quote_from_notification
from app.client.quote.models import Quote
from app.services.api_server.requests import custom_filters
from app.services.errors.exceptions import NotFoundError


def create_notification(schema=None):
    dict_body = request.get_json()
    item = Notification().create_item(dict_body).save()
    if schema:
        item = NotificationSchema().dump(item)
    return item


def get_notification(id, schema=None, columns=None):
    query = Notification.query
    if columns:
        query = query.with_entities(*[getattr(Notification, column) for column in columns])
    item = query.filter(Notification.id == id).first()
    if not item:
        raise NotFoundError()
    if schema:
        item = NotificationSchema().dump(item)
    return item


def gets_notification(schema=None, columns=None, filters=None, user_id=None):
    dict_filters = custom_filters()
    query = Notification.query.filter(Notification.deleted_at == None)
    if columns:
        query = query.with_entities(*[getattr(Notification, column) for column in columns])
    if filters:
        for key in filters:
            query = query.filter(getattr(Notification, key) == filters[key])
    if user_id is not None:
        query = query.join(Quote, Quote.id == Notification.quote_id).filter(Quote.user_id == user_id)
    items = query.paginate(dict_filters["page"], dict_filters["per_page"], False)
    items_paginate = items
    if schema:
        items = NotificationSchema(many=True).dump(items.items)

    return items, items_paginate


def gets_user_notification(user_id, schema=None, columns=None, filters=None):
    dict_filters = custom_filters()
    query = NotificationSend.query.filter(NotificationSend.user_id == user_id,
                                          NotificationSend.deleted_at.is_(None))
    if columns:
        query = query.with_entities(*[getattr(NotificationSend, column) for column in columns])
    if filters:
        for key in filters:
            query = query.filter(getattr(NotificationSend, key) == filters[key])

    items = query.paginate(dict_filters["page"], dict_filters["per_page"], False)
    for item in items.items:
        item.quote = get_quote_from_notification(item.notification_id)
    items_paginate = items
    if schema:
        items = NotificationSchema(many=True).dump(items.items)

    return items, items_paginate


def update_notification(id, schema=None):
    item = get_notification(id)
    dict_body = request.get_json()
    item.update_item(dict_body).update()
    if schema:
        item = NotificationSchema().dump(item)
    return item


def delete_notification(id):
    item = get_notification(id)
    item.delete()
    return True
