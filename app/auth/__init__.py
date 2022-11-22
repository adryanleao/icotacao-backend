from flask import Blueprint

bp = Blueprint("auth_bp", __name__)

from . import views

def init_app(app):
    app.register_blueprint(bp, url_prefix="/auth")
