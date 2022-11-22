from flask import request
from flask_jwt_extended import jwt_required

from app.admin.notification.services.crud import get_notification, gets_notification, \
    gets_user_notification
from app.auth.services.user import get_user_jwt
from app.client.notification import bp
from app.services.api_server.requests import default_return


@bp.route("/<item_id>", methods=["GET"])
@jwt_required()
def item_view(item_id):
    try:
        if request.method == 'GET':
            item = get_notification(item_id, True)
            return default_return(200, 2, item)
    except Exception as e:
        raise e


@bp.route("", methods=["GET"])
@jwt_required()
def item_views():
    try:
        if request.method == 'GET':
            items, items_paginate = gets_notification(True)
            return default_return(200, 2, items, items_paginate)
    except Exception as e:
        raise e


@bp.route("/my_notifications", methods=["GET"])
@jwt_required()
def item_notifications():
    try:
        if request.method == 'GET':
            user_jwt = get_user_jwt()
            items, items_paginate = gets_user_notification(user_jwt["user_id"], True)
            return default_return(200, 2, items, items_paginate)
    except Exception as e:
        raise e

