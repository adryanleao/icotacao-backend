from flask import request

from app.admin.segment.models import Segment
from app.admin.segment.schemas import SegmentSchema
from app.services.api_server.requests import custom_filters
from app.services.errors.exceptions import NotFoundError


def gets_segment(schema=None, columns=None, filters=None):
    dict_filters = custom_filters()
    query = Segment.query.filter(Segment.deleted_at == None)
    if columns:
        query = query.with_entities(*[getattr(Segment, column) for column in columns])
    if filters:
        for key in filters:
            query = query.filter(getattr(Segment, key) == filters[key])
    if dict_filters["search"]:
        query = query.filter(Segment.name.like(f'%%{dict_filters["search"]}%%'))
    items = query.paginate(dict_filters["page"], dict_filters["per_page"], False)
    items_paginate = items
    if schema:
        items = SegmentSchema(many=True).dump(items.items)

    return items, items_paginate


def get_segment(id, schema=None, columns=None, exclude=[]):
    query = Segment.query
    if columns:
        query = query.with_entities(*[getattr(Segment, column) for column in columns])
    item = query.filter(Segment.id == id).first()
    if not item:
        raise NotFoundError()
    if schema:
        item = SegmentSchema(exclude=exclude).dump(item)
    return item


def create_segment(schema=None, exclude=[]):
    dict_body = request.get_json()

    item = Segment().create_item(dict_body).save()

    item = get_segment(item.id, schema, exclude=exclude)

    return item


def update_segment(id, schema=None, exclude=[]):
    item = get_segment(id)
    dict_body = request.get_json()
    item.update_item(dict_body).update()
    if schema:
        item = SegmentSchema(exclude=exclude).dump(item)
    return item


def delete_segment(id):
    item = get_segment(id)
    item.delete()
    return True
