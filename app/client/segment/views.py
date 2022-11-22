from flask import request

from app.admin.segment.services.crud import gets_segment, get_segment
from app.client.segment import bp
from app.services.api_server.requests import default_return


@bp.route("/<item_id>", methods=["GET"])
def item_view(item_id):
    try:
        if request.method == 'GET':
            item = get_segment(item_id, schema=True)
            return default_return(200, 2, item)
    except Exception as e:
        raise e


@bp.route("", methods=["GET"])
def item_views():
    try:
        if request.method == 'GET':
            items, items_paginate = gets_segment(True)
            return default_return(200, 2, items, items_paginate)
    except Exception as e:
        raise e
