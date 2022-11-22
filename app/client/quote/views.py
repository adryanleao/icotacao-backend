from flask_jwt_extended import jwt_required

from app.client.quote import bp
from app.client.quote.services.crud import gets_quote, delete_quote, \
    update_quote, get_quote, \
    create_quote_products, create_quote
from app.client.quote.services.proposal import *
from app.services.annotations.logged_admin import user_logged_admin
from app.services.api_server.requests import default_return
from app.services.files.proposal_products_csv import proposal_products_csv
from app.services.files.quote_products_csv import quote_products_csv


@bp.route("", methods=["GET", "POST"])
@jwt_required()
def item_views():
    try:
        if request.method == 'GET':
            user_jwt = get_user_jwt()
            items, items_paginate = gets_quote(True, user=user_jwt)
            return default_return(200, 2, items, items_paginate)

        if request.method == 'POST':
            item = create_quote(schema=True)
            return default_return(201, 1, item)
    except Exception as e:
        raise e


@bp.route("/<item_id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
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


@bp.route("/<item_id>/products", methods=["POST"])
@jwt_required()
@user_logged_admin
def item_products(item_id):
    try:
        if request.method == 'POST':
            payload = create_quote_products(item_id)
            return default_return(payload["content"], payload["code"],
                                  payload["message"])
    except Exception as e:
        raise e


@bp.route("/<item_id>/proposals", methods=["POST", "GET"])
@jwt_required()
def item_proposal_list(item_id):
    try:
        if request.method == 'POST':
            item = create_quote_proposal(item_id, True)
            return default_return(201, 1, item)

        if request.method == 'GET':
            items, items_paginate = gets_quote_proposal(item_id, True)
            return default_return(200, 2, items, items_paginate)
    except Exception as e:
        raise e


@bp.route("/my_quotes", methods=["GET"])
@jwt_required()
def item_quotes():
    try:
        if request.method == 'GET':
            user_jwt = get_user_jwt()
            items, items_paginate = gets_quote(True, user=user_jwt)
            return default_return(200, 2, items, items_paginate)
    except Exception as e:
        raise e


@bp.route("/proposals/<item_id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def item_proposal(item_id):
    try:
        if request.method == 'GET':
            item = get_quote_proposal(item_id, True)
            return default_return(200, 2, item)

        if request.method == 'PUT':
            item = update_quote_proposal(item_id, schema=True)
            return default_return(200, 3, item)

        if request.method == 'DELETE':
            delete_quote_proposal(item_id)
            return default_return(204, 4, {})
    except Exception as e:
        raise e


@bp.route("/files", methods=["POST"])
@jwt_required()
def item_file_resource():
    try:
        if request.method == 'POST':
            item = quote_products_csv()
            return default_return(200, 2, item)
    except Exception as e:
        raise e


@bp.route("/proposal/files", methods=["POST"])
@jwt_required()
def proposal_file_resource():
    try:
        if request.method == 'POST':
            item = proposal_products_csv()
            return default_return(200, 2, item)
    except Exception as e:
        raise e
