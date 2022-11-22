from flask_jwt_extended import jwt_required

from app.auth import bp
from app.auth.services.validations import validate_token, \
    validate_refresh_token


@bp.route("/token", methods=["POST"])
def item_view():
    try:
        return validate_token()
    except Exception as e:
        raise e


@bp.route("/refresh", methods=["GET", "POST"])
@jwt_required(refresh=True)
def item_views():
    try:
        return validate_refresh_token()
    except Exception as e:
        raise e


@bp.route("/health", methods=["GET"])
def get_health():
    return 200
