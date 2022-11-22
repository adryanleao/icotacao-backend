from flask import request
from flask_jwt_extended import jwt_required

from app.auth.services.user import get_user_jwt
from app.client.costumer import bp
from app.client.costumer.services.crud import get_costumer, update_costumer, delete_costumer, gets_costumer, \
    create_costumer
from app.services.api_server.requests import default_return


@bp.route("/<item_id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def item_view(item_id):
    try:
        if request.method == 'GET':
            item = get_costumer(item_id, True)
            return default_return(200, 2, item)

        if request.method == 'PUT':
            item = update_costumer(item_id, True)
            return default_return(200, 3, item)

        if request.method == 'DELETE':
            delete_costumer(item_id)
            return default_return(204, 4)
    except Exception as e:
        raise e


@bp.route("", methods=["GET", "POST"])
@jwt_required()
def item_views():
    try:
        if request.method == 'GET':
            user_jwt = get_user_jwt()
            items, items_paginate = gets_costumer(True, user_id=user_jwt["user_id"])
            return default_return(200, 2, items, items_paginate)

        if request.method == 'POST':
            user_jwt = get_user_jwt()
            item = create_costumer(True, user_id=user_jwt["user_id"])
            return default_return(201, 1, item)
    except Exception as e:
        raise e
