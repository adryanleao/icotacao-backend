from flask import request
from sqlalchemy import or_

from app.admin.city.models import City
from app.admin.city.schemas import CitySchema
from app.services.api_server.requests import custom_filters
from app.services.errors.exceptions import NotFoundError


def create_city(schema=None):
    dict_body = request.get_json()
    item = City().create_item(dict_body).save()
    if schema:
        item = CitySchema().dump(item)
    return item


def get_city(id, schema=None, columns=None):
    query = City.query
    if columns:
        query = query.with_entities(*[getattr(City, column) for column in columns])
    item = query.filter(City.id == id).first()
    if not item:
        raise NotFoundError()
    if schema:
        item = CitySchema().dump(item)
    return item


def gets_city(schema=None, columns=None):
    dict_filters = custom_filters()
    query = City.query.filter(City.deleted_at == None)
    if columns:
        query = query.with_entities(*[getattr(City, column) for column in columns])
    if dict_filters["search"]:
        query = query.filter(
            or_(City.name.like(f'%%{dict_filters["search"]}%%')))
    items = query.paginate(dict_filters["page"], dict_filters["per_page"], False)
    items_paginate = items
    if schema:
        items = CitySchema(many=True).dump(items.items)

    return items, items_paginate


def update_city(id, schema=None):
    item = get_city(id)
    dict_body = request.get_json()
    item.update_item(dict_body).update()
    if schema:
        item = CitySchema().dump(item)
    return item


def delete_city(id):
    item = get_city(id)
    item.delete()
    return True
