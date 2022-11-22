from flask import Blueprint

bp = Blueprint("user_client", __name__)

from . import views

def init_app(app):
    app.register_blueprint(bp, url_prefix="/v1/client")

    from app.client import counts
    counts.init_app(app)

    from app.client import costumer
    costumer.init_app(app)

    from app.client import quote
    quote.init_app(app)

    from app.client import segment
    segment.init_app(app)

    from app.client import notification
    notification.init_app(app)