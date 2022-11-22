from flask import request
from flask_jwt_extended import jwt_required

from app.admin.notification import bp
from app.admin.notification.services.crud import get_notification, update_notification, delete_notification, gets_notification, \
    create_notification
from app.services.api_server.requests import default_return


@bp.route("/<item_id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def item_view(item_id):
    try:
        if request.method == 'GET':
            item = get_notification(item_id, True)
            return default_return(200, 2, item)

        if request.method == 'PUT':
            item = update_notification(item_id, True)
            return default_return(200, 3, item)

        if request.method == 'DELETE':
            delete_notification(item_id)
            return default_return(204, 4)
    except Exception as e:
        raise e


@bp.route("", methods=["GET", "POST"])
@jwt_required()
def item_views():
    try:
        if request.method == 'GET':
            items, items_paginate = gets_notification(True)
            return default_return(200, 2, items, items_paginate)

        if request.method == 'POST':
            item = create_notification(schema=True)
            return default_return(201, 1, item)
    except Exception as e:
        raise e

