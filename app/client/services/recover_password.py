import uuid

from flask import request

from config import Config
from app.admin.user.models import User
from app.services.email.send_email import send_email
from app.services.errors.exceptions import UnauthorizedError, GenerateError


def recover_user_email():
    dict_body = request.get_json()
    email = dict_body.get("email")

    if not email:
        raise GenerateError("E-mail não enviado!", 400)

    item = User.query.filter(User.email == email,
                             User.deleted_at == None).first()

    if not item:
        raise UnauthorizedError('Usuário não encontrado!')

    # NEW PASSWORD
    token = uuid.uuid1()

    # UPDATE USER
    item.token_update = str(token)
    item.update()

    # SEND PASSWORD
    subject = "Resetar Senha"
    template = "email/reset.html"
    to = item.email
    content = item
    content.redirect_url = f"{Config.SITE_HTTPS}/auth/hash_confirm?hash={item.token_update}"
    send_email(to, subject, content=content, template=template)

    return True


def hash_validate():
    dict_body = request.get_json()

    try:
        dict_body['hash']
    except:
        raise UnauthorizedError('Acesso Negado')

    item = User.query.filter(User.token_update == dict_body['hash']).first()

    if item is not None:
        return {"data": True}
    else:
        return {"data": False}


def recover_password():
    dict_body = request.get_json()

    try:
        dict_body['hash']
    except:
        raise UnauthorizedError('Acesso Negado')

    item = User.query.filter(User.token_update == dict_body['hash']).first()
    if item is not None:
        item.set_password(dict_body['password'])
        item.token_update = str(uuid.uuid1())
        item.update()
    else:
        raise UnauthorizedError('Acesso Negado')

    return True
