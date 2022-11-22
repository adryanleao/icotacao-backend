from flask import Flask
from app.services.sqlalchemy.extensions import db, migrate, jwt, ma, cache, \
    cors


def create_app():
    """create and configure the flask application"""
    # app
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # extension
    cors.init_app(app, resources={r"/*": {"origins": "*"}})
    cache.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    ma.init_app(app)

    @app.route("/", methods=["GET"])
    def index():
        return "ok", 200

    # errors
    from app.services.errors.exceptions import exception_handler_bp
    app.register_blueprint(exception_handler_bp)

    # auth
    from app import auth
    auth.init_app(app)

    # routes admin
    from app import admin
    admin.init_app(app)

    # routes client
    from app import client
    client.init_app(app)

    return app
