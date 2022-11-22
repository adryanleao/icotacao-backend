from app.admin.user.schemas import UserSchema
from flask import request

from app.admin.company.services.crud import create_company, update_company
from app.admin.user.services.crud import create_user, get_user, update_user
from app.admin.user.services.validations import validate_email, validate_taxpayer
from app.services.errors.exceptions import UnauthorizedError


def create_client_and_company():
    dict_body = request.get_json()

    # validate email is exist
    is_email = validate_email(dict_body["email"])
    if is_email:
        raise UnauthorizedError("Email já cadastrado no sistema!")

    # validate cpf is exist
    is_taxpayer = validate_taxpayer(dict_body["cpf"])
    if is_taxpayer:
        raise UnauthorizedError("CPF já cadastrado no sistema!")

    # create company
    if "company" in dict_body:
        company = create_company(True)
        dict_body["company_id"] = company["id"]

    # create user
    user = create_user(True, dict_body, exclude=["id"])

    if "company" in dict_body:
        # union user company return
        user["company"] = company

    return user


def update_client_and_company(user_id, schema=None):
    dict_body = request.get_json()

    # update user
    user = update_user(user_id, schema=False, exclude=["id"])

    # update company
    if "company" in dict_body and dict_body["company"]:
        if user.company is None:
            company = create_company()
            user.company_id = company.id
            user.update()
        else:
            company = update_company(user.company_id, schema, exclude=["id"])
    item = user
    if schema:
        item = UserSchema().dump(user)

    return item
