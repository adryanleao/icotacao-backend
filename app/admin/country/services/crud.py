from flask import request
from sqlalchemy import or_

from app.admin.country.models import Country
from app.admin.country.schemas import CountrySchema
from app.services.api_server.requests import custom_filters
from app.services.errors.exceptions import NotFoundError


def create_country(schema=None):
    dict_body = request.get_json()
    item = Country().create_item(dict_body).save()
    if schema:
        item = CountrySchema().dump(item)
    return item


def get_country(id, schema=None, columns=None):
    query = Country.query
    if columns:
        query = query.with_entities(*[getattr(Country, column) for column in columns])
    item = query.filter(Country.id == id).first()
    if not item:
        raise NotFoundError()
    if schema:
        item = CountrySchema().dump(item)
    return item


def gets_country(schema=None, columns=None):
    page, per_page, search = custom_filters()
    query = Country.query.filter(Country.deleted_at == None)
    if columns:
        query = query.with_entities(*[getattr(Country, column) for column in columns])
    if search:
        query = query.filter(
            or_(Country.name.like(f'%%{search}%%')))
    items = query.paginate(page, per_page, False)
    items_paginate = items
    if schema:
        items = CountrySchema(many=True).dump(items.items)

    return items, items_paginate


def update_country(id, schema=None):
    item = get_country(id)
    dict_body = request.get_json()
    item.update_item(dict_body).update()
    if schema:
        item = CountrySchema().dump(item)
    return item


def delete_country(id):
    item = get_country(id)
    item.delete()
    return True
