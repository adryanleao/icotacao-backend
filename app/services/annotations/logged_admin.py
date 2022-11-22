from functools import wraps

from flask_jwt_extended import get_jwt_identity

from app.services.errors.exceptions import UnauthorizedError


def user_logged_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        jwt_group_id = get_jwt_identity()['group_id']

        if jwt_group_id == 5:
            raise UnauthorizedError('Usuário não autorizado!')

        return f(*args, **kwargs)

    return wrap
