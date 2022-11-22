from flask import request
from sqlalchemy import or_

from app.admin.group.models import Group
from app.admin.group.schemas import GroupSchema
from app.services.api_server.requests import custom_filters
from app.services.errors.exceptions import NotFoundError


def create_group(schema=None):
    dict_body = request.get_json()
    item = Group().create_item(dict_body).save()
    if schema:
        item = GroupSchema().dump(item)
    return item


def get_group(id, schema=None, columns=None):
    query = Group.query
    if columns:
        query = query.with_entities(*[getattr(Group, column) for column in columns])
    item = query.filter(Group.id == id).first()
    if not item:
        raise NotFoundError()
    if schema:
        item = GroupSchema().dump(item)
    return item


def gets_group(schema=None, columns=None):
    page, per_page, search = custom_filters()
    query = Group.query.filter(Group.deleted_at == None)
    if columns:
        query = query.with_entities(*[getattr(Group, column) for column in columns])
    if search:
        query = query.filter(
            or_(Group.name.like(f'%%{search}%%')))
    items = query.paginate(page, per_page, False)
    items_paginate = items
    if schema:
        items = GroupSchema(many=True).dump(items.items)

    return items, items_paginate


def update_group(id, schema=None):
    item = get_group(id)
    dict_body = request.get_json()
    item.update_item(dict_body).update()
    if schema:
        item = GroupSchema().dump(item)
    return item


def delete_group(id):
    item = get_group(id)
    item.delete()
    return True
