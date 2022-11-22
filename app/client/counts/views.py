from flask import request
from flask_jwt_extended import jwt_required

from app.auth.services.user import get_user_jwt
from app.client.counts import bp
from app.client.counts.services.counts import count_notifications_and_quotes
from app.services.api_server.requests import default_return


@bp.route("", methods=["GET"])
@jwt_required()
def item_views():
    try:
        if request.method == 'GET':
            user_jwt = get_user_jwt()
            items = count_notifications_and_quotes(user_jwt["user_id"])
            return default_return(200, 2, items)
    except Exception as e:
        raise e
