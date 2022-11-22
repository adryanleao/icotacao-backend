from flask_jwt_extended import get_jwt_identity

from app.admin.user.services.hash import decrypt_user_id


def get_user_jwt():
    user_jwt = get_jwt_identity()
    user_jwt["user_id"] = decrypt_user_id(user_jwt["hash_id"])
    return user_jwt
