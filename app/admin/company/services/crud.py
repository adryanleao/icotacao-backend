from flask import request

from app.admin.company.models import Company
from app.admin.company.schemas import CompanySchema
from app.admin.company.services.segments import create_segment_company, update_segment_company
from app.services.api_server.requests import custom_filters
from app.services.errors.exceptions import NotFoundError


def create_company(schema=None, exclude=[]):
    dict_body = request.get_json()

    if "company" in dict_body:
        dict_body = dict_body["company"]

    item = Company().create_item(dict_body).save()

    if "segments" in dict_body:
        create_segment_company(item.id, dict_body["segments"])

    # pega company totalmente atualizado
    item = get_company(item.id, schema, exclude=exclude)

    return item


def get_company(id, schema=None, columns=None, exclude=[]):
    query = Company.query
    if columns:
        query = query.with_entities(*[getattr(Company, column) for column in columns])
    item = query.filter(Company.id == id).first()
    if not item:
        raise NotFoundError()
    if schema:
        item = CompanySchema(exclude=exclude).dump(item)
    return item


def gets_company(schema=None, columns=None, filters=None):
    dict_filters = custom_filters()
    query = Company.query.filter(Company.deleted_at == None)
    if columns:
        query = query.with_entities(*[getattr(Company, column) for column in columns])
    if filters:
        for key in filters:
            query = query.filter(getattr(Company, key) == filters[key])
    if dict_filters["search"]:
        query = query.filter(Company.name.like(f'%%{dict_filters["search"]}%%'))
    items = query.paginate(dict_filters["page"], dict_filters["per_page"], False)
    items_paginate = items
    if schema:
        items = CompanySchema(many=True).dump(items.items)

    return items, items_paginate


def update_company(id, schema=None, exclude=[]):
    item = get_company(id)
    dict_body = request.get_json()
    if "company" in dict_body:
        dict_body = dict_body["company"]
    item.update_item(dict_body).update()

    if "segments" in dict_body:
        update_segment_company(item.id, dict_body["segments"])

    if schema:
        item = CompanySchema(exclude=exclude).dump(item)
    return item


def delete_company(id):
    item = get_company(id)
    item.delete()
    return True
