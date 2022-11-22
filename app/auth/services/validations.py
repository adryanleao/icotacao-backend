from flask import request

from app.admin.user.models import User
from app.admin.user.services.crud import get_user
from app.auth.services.token import generate_user_jwt
from app.auth.services.user import get_user_jwt
from app.services.errors.exceptions import UnauthorizedError


def validate_token():
    basic = request.headers.get("Authorization", None)
    params = request.get_json()

    try:
        if not basic:
            raise UnauthorizedError("Invalid Basic Negado Header")

        if params["grant_type"] != "password":
            raise UnauthorizedError("Invalid grant type")

        username = params["username"]
        password = params["password"]
    except:
        raise UnauthorizedError("Alguma coisa deu errado")

    user = User.query.filter(User.deleted_at.is_(None), User.status == 1)

    if basic == "NDRleHByZXNzYWRtaW46NDRleHByZXNzcGFzc3dvcmQ=":
        user = user.filter(User.group_id.in_([4, 5]))
    elif basic == "b2ZlcnRhcGxheXVzZXI6b2ZlcnRhcGxheXBhc3N3b3Jk":
        user = user.filter(User.group_id.notin_([4, 5]))
    else:
        raise UnauthorizedError("Invalid Basic Negado")

    if "@" in username:
        user = user.filter(User.email == username)
    else:
        user = user.filter(User.cpf == username)

    user = user.first()

    if user is not None and user.check_password(password):
        token = generate_user_jwt(user)
        token["user"] = get_user(user.id, True)

        return token, 200
    else:
        raise UnauthorizedError("Usuário ou Senha incorreta!")


def validate_refresh_token():
    try:
        user_jwt = get_user_jwt()
        user = get_user(user_jwt["user_id"])

        if user:
            token = generate_user_jwt(user)

            return token, 200
        else:
            raise UnauthorizedError("Usuário não autorizado!")
    except UnauthorizedError as e:
        return {"Error": str(e)}, 401
    except Exception as e:
        return {"Error": str(e)}, 500
