from flask_jwt_extended import jwt_required

from app.admin.dashboard import bp
from app.admin.dashboard.services.crud import get_dashboard
from app.services.api_server.requests import default_return


@bp.route("", methods=["GET"])
@jwt_required()
def item_views():
    try:
        item = get_dashboard()
        return default_return(200, 2, item)
    except Exception as e:
        raise e
