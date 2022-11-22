from flask import request
from sqlalchemy import or_

from app.admin.state.models import State
from app.admin.state.schemas import StateSchema
from app.services.api_server.requests import custom_filters
from app.services.errors.exceptions import NotFoundError


def create_state(schema=None):
    dict_body = request.get_json()
    item = State().create_item(dict_body).save()
    if schema:
        item = StateSchema().dump(item)
    return item


def get_state(id, schema=None, columns=None):
    query = State.query
    if columns:
        query = query.with_entities(*[getattr(State, column) for column in columns])
    item = query.filter(State.id == id).first()
    if not item:
        raise NotFoundError()
    if schema:
        item = StateSchema().dump(item)
    return item


def gets_state(schema=None, columns=None):
    page, per_page, search = custom_filters()
    query = State.query.filter(State.deleted_at == None)
    if columns:
        query = query.with_entities(*[getattr(State, column) for column in columns])
    if search:
        query = query.filter(
            or_(State.name.like(f'%%{search}%%')))
    items = query.paginate(page, per_page, False)
    items_paginate = items
    if schema:
        items = StateSchema(many=True).dump(items.items)

    return items, items_paginate


def update_state(id, schema=None):
    item = get_state(id)
    dict_body = request.get_json()
    item.update_item(dict_body).update()
    if schema:
        item = StateSchema().dump(item)
    return item


def delete_state(id):
    item = get_state(id)
    item.delete()
    return True
