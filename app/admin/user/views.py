from flask import request
from flask_jwt_extended import jwt_required

from app.admin.user import bp
from app.admin.user.services.crud import get_user, update_user, delete_user, \
    gets_user, \
    create_user
from app.admin.user.services.image import create_user_image
from app.services.api_server.requests import default_return


@bp.route("/<item_id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def item_view(item_id):
    try:
        if request.method == 'GET':
            item = get_user(item_id, True)
            return default_return(200, 2, item)

        if request.method == 'PUT':
            item = update_user(item_id, True)
            return default_return(200, 3, item)

        if request.method == 'DELETE':
            delete_user(item_id)
            return default_return(204, 4)
    except Exception as e:
        raise e


@bp.route("", methods=["GET", "POST"])
@jwt_required()
def item_views():
    try:
        if request.method == 'GET':
            items, items_paginate = gets_user(True)
            return default_return(200, 2, items, items_paginate)

        if request.method == 'POST':
            item = create_user(True)
            return default_return(201, 1, item)
    except Exception as e:
        raise e


@bp.route("/<item_id>/images", methods=["POST"])
@jwt_required()
def item_image(item_id):
    try:
        if request.method == 'POST':
            item = get_user(item_id)
            image_return = create_user_image(item)
            return default_return(200, 2, image_return)
    except Exception as e:
        raise e
