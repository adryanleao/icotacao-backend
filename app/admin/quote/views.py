from flask import request
from flask_jwt_extended import jwt_required

from app.admin.quote import bp
from app.client.quote.services.crud import get_quote, update_quote, \
    delete_quote, gets_quote, create_quote
from app.services.annotations.logged_admin import user_logged_admin
from app.services.api_server.requests import default_return


@bp.route("/<item_id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
@user_logged_admin
def item_view(item_id):
    try:
        if request.method == 'GET':
            item = get_quote(item_id, True)
            return default_return(200, 2, item)

        if request.method == 'PUT':
            item = update_quote(item_id, True)
            return default_return(200, 3, item)

        if request.method == 'DELETE':
            delete_quote(item_id)
            return default_return(204, 4)
    except Exception as e:
        raise e


@bp.route("", methods=["GET", "POST"])
@jwt_required()
@user_logged_admin
def item_views():
    try:
        if request.method == 'GET':
            items, items_paginate = gets_quote(True)
            return default_return(200, 2, items, items_paginate)

        if request.method == 'POST':
            item = create_quote(schema=True)
            return default_return(201, 1, item)
    except Exception as e:
        raise e
