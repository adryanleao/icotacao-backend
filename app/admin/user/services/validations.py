from flask import request

from app.admin.user.models import User
from app.admin.user.schemas import UserSchema


def validate_taxpayer(taxpayer=None, schema=None):
    if taxpayer is None:
        taxpayer = request.args.get("taxpayer")
    user_taxpayer = User.query.filter(User.cpf == taxpayer, User.deleted_at == None).first()
    if user_taxpayer:
        if schema:
            return UserSchema().dump(user_taxpayer)
        else:
            return user_taxpayer


def validate_email(email=None, schema=None):
    if email is None:
        email = request.args.get("email")
    user_email = User.query.filter(User.email == email, User.deleted_at == None).first()
    if user_email:
        if schema:
            return UserSchema().dump(user_email)
        else:
            return user_email
