from flask import request

from app.services.api_server.status import code_http, code_message
from app.services.sqlalchemy.pagination import pagination_info


def custom_filters():
    return {
        "page": request.args.get("page", default=1, type=int),
        "per_page": request.args.get("per_page", default=12, type=int),
        "search": request.args.get("search"),
        "filter": request.args.get("filter"),
        "created_at_start": request.args.get("created_at_start", default=None),
        "created_at_end": request.args.get("created_at_end", default=None),
        "order_by_column": request.args.get("order_by_column", default="id", type=str),
        "order_by_direction": request.args.get("order_by_direction", default=None, type=str)
    }


def default_return(status=200, message=2, data={}, items_paginate={}, summary={}):
    pagination = pagination_info(items_paginate)

    return {
               "status": code_http(status), "msg": code_message(message), "pagination": pagination,
               "summary": summary, "data": data
           }, status, {'Content-Type': 'application/json'}
