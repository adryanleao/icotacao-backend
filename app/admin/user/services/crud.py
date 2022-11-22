import json
from flask import request
from sqlalchemy import or_

from app.admin.user.models import User, UserAddress
from app.admin.user.schemas import UserSchema
from app.services.api_server.requests import custom_filters
from app.services.errors.exceptions import NotFoundError


def create_user(schema=None, dict_body=None, exclude=[]):
    if dict_body is None:
        dict_body = request.get_json()
    item = User().create_item(dict_body).save()
    if 'address' in dict_body:
        dict_body['address']['user_id'] = item.id
        UserAddress().create_item(dict_body["address"]).save()
    if schema:
        item = UserSchema(exclude=exclude).dump(item)
    return item


def get_user(id=None, schema=None, columns=None, exclude=[]):
    query = User.query
    if columns:
        query = query.with_entities(
            *[getattr(User, column) for column in columns])
    if id:
        query = query.filter(or_(User.id == id))

    item = query.first()
    if not item:
        raise NotFoundError()
    if schema:
        item = UserSchema(exclude=exclude).dump(item)
    return item


def gets_user(schema=None, columns=None, filters=None):
    dict_filters = custom_filters()
    query = User.query.filter(User.deleted_at == None)

    if filters == None:
        filters = json.loads(dict_filters['filter'])

    if columns:
        query = query.with_entities(
            *[getattr(User, column) for column in columns])
    if filters:
        for key in filters:
            if type(filters[key]) == list:
                query = query.filter(getattr(User, key).in_(filters[key]))
            else:
                query = query.filter(getattr(User, key) == filters[key])
    if dict_filters["search"]:
        query = query.filter(
            or_(User.name.like(f'%%{dict_filters["search"]}%%'),
                User.email.like(f'%%{dict_filters["search"]}%%'),
                User.cpf.like(f'%%{dict_filters["search"]}%%')))
    items = query.paginate(dict_filters["page"], dict_filters["per_page"],
                           False)
    items_paginate = items
    if schema:
        items = UserSchema(many=True).dump(items.items)

    return items, items_paginate


def update_user(id, schema=None, exclude=[]):
    item = get_user(id)
    dict_body = request.get_json()
    item.update_item(dict_body).update()
    if schema:
        item = UserSchema(exclude=exclude).dump(item)
    return item


def delete_user(id):
    item = get_user(id)
    item.delete()
    return True
