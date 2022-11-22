from flask import request
from flask_jwt_extended import jwt_required

from app.admin.user.services.crud import get_user, delete_user
from app.admin.user.services.validations import validate_taxpayer, \
    validate_email
from app.auth.services.user import get_user_jwt
from app.client import bp
from app.client.services.crud import create_client_and_company, \
    update_client_and_company
from app.client.services.recover_password import recover_user_email, \
    hash_validate, recover_password
from app.services.address.validate import validate_address_by_code_post
from app.services.api_server.requests import default_return


@bp.route("", methods=["POST"])
def item_post_views():
    try:
        if request.method == 'POST':
            item = create_client_and_company()
            return default_return(201, 1, item)

    except Exception as e:
        raise e


@bp.route("", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def item_views():
    try:
        user_jwt = get_user_jwt()
        if request.method == 'GET':
            item = get_user(user_jwt["user_id"], True)
            return default_return(200, 2, item)

        if request.method == 'PUT':
            item = update_client_and_company(user_jwt["user_id"], True)
            return default_return(200, 2, item)

        if request.method == 'DELETE':
            delete_user(user_jwt["user_id"])
            return default_return(204, 4)
    except Exception as e:
        raise e


@bp.route("/address/validate", methods=["GET"])
def item_address():
    try:
        if request.method == 'GET':
            item = validate_address_by_code_post()
            return default_return(200, 2, item)
    except Exception as e:
        raise e


@bp.route("/cpf/validate", methods=["GET"])
def item_validate():
    try:
        if request.method == 'GET':
            item = validate_taxpayer(schema=True)
            return default_return(200, 2, item)
    except Exception as e:
        raise e


@bp.route("/email/validate", methods=["GET"])
def item_email_validate():
    try:
        item = validate_email(schema=True)
        return default_return(200, 2, item)
    except Exception as e:
        raise e


@bp.route("/recover", methods=["POST"])
def item_recover():
    try:
        if request.method == 'POST':
            recover_user_email()
            msg = "E-mail enviado com sucesso! Verifique sua caixa de e-mail!"
            return default_return(200, msg)
    except Exception as e:
        raise e


@bp.route("/recover/password", methods=["POST"])
def item_recover_password():
    try:
        if request.method == 'POST':
            data = recover_password()
            return default_return(200, 2, data)
    except Exception as e:
        raise e


@bp.route("/hash/validate", methods=["POST"])
def item_hash_validate():
    try:
        if request.method == 'POST':
            data = hash_validate()
            return default_return(200, 2, data)
    except Exception as e:
        raise e
