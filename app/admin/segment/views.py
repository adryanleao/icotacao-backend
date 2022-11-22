from flask import request
from flask_jwt_extended import jwt_required

from app.admin.segment import bp
from app.admin.segment.services.crud import gets_segment, delete_segment, get_segment, update_segment, create_segment
from app.services.annotations.logged_admin import user_logged_admin
from app.services.api_server.requests import default_return


@bp.route("/<item_id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
@user_logged_admin
def item_view(item_id):
    try:
        if request.method == 'GET':
            item = get_segment(item_id, True)
            return default_return(200, 2, item)

        if request.method == 'PUT':
            item = update_segment(item_id, True)
            return default_return(200, 3, item)

        if request.method == 'DELETE':
            delete_segment(item_id)
            return default_return(204, 4)
    except Exception as e:
        raise e


@bp.route("", methods=["GET", "POST"])
@jwt_required()
@user_logged_admin
def item_views():
    try:
        if request.method == 'GET':
            items, items_paginate = gets_segment(True)
            return default_return(200, 2, items, items_paginate)

        if request.method == 'POST':
            item = create_segment(schema=True)
            return default_return(201, 1, item)
    except Exception as e:
        raise e

