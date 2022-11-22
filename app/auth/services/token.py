from flask_jwt_extended import create_access_token, create_refresh_token

from app.admin.user.services.hash import encrypt_user_id
from config import Config


def generate_user_jwt(user):
    user_jwt = {
        "hash_id": encrypt_user_id(user.id),
        "name": user.name,
        "group_id": user.group_id,
        "company_id": user.company_id
    }

    access_token = create_access_token(identity=user_jwt)
    refresh_token = create_refresh_token(identity=user_jwt)
    data = {
        "token_type": "Bearer",
        "expires_in": Config.JWT_EXPIRES,
        "access_token": access_token,
        "refresh_token": refresh_token
    }
    return data
