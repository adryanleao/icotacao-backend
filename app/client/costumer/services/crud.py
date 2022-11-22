from flask import request
from sqlalchemy import or_

from app.client.costumer.models import Costumer, CostumerAddress
from app.client.costumer.schemas import CostumerSchema
from app.services.api_server.requests import custom_filters
from app.services.errors.exceptions import NotFoundError


def create_costumer(schema=None, user_id=None):
    dict_body = request.get_json()
    if user_id:
        dict_body["user_id"] = user_id
    item = Costumer().create_item(dict_body).save()
    if 'address' in dict_body:
        dict_body['address']['costumer_id'] = item.id
        CostumerAddress().create_item(dict_body["address"]).save()
    if schema:
        item = CostumerSchema().dump(item)
    return item


def get_costumer(id, schema=None, columns=None):
    query = Costumer.query
    if columns:
        query = query.with_entities(
            *[getattr(Costumer, column) for column in columns])
    item = query.filter(Costumer.id == id).first()
    if not item:
        raise NotFoundError()
    if schema:
        item = CostumerSchema().dump(item)
    return item


def gets_costumer(schema=None, columns=None, user_id=None):
    dict_filters = custom_filters()
    query = Costumer.query.filter(Costumer.deleted_at == None)
    if columns:
        query = query.with_entities(
            *[getattr(Costumer, column) for column in columns])
    if user_id:
        query = query.filter(Costumer.user_id == user_id)
    if dict_filters["search"]:
        query = query.filter(
            or_(Costumer.name.like(f'%%{dict_filters["search"]}%%'),
                Costumer.tax_payer.like(f'%%{dict_filters["search"]}%%')))
    items = query.paginate(dict_filters["page"], dict_filters["per_page"],
                           False)
    items_paginate = items
    if schema:
        items = CostumerSchema(many=True).dump(items.items)

    return items, items_paginate


def update_costumer(id, schema=None):
    item = get_costumer(id)
    dict_body = request.get_json()
    item.update_item(dict_body).update()
    if 'address' in dict_body:
        dict_body['address']['costumer_id'] = item.id
        CostumerAddress().update_item(dict_body["address"]).update()
    if schema:
        item = CostumerSchema().dump(item)
    return item


def delete_costumer(id):
    item = get_costumer(id)
    item.delete()
    return True
