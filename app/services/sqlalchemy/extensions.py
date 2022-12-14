from datetime import datetime
from flask import current_app
from flask_caching import Cache
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy, Model, get_state
from sqlalchemy import orm
from flask_migrate import Migrate
from functools import partial

import boto3

from config import Config


class CRUDMixin(Model):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        self.deleted_at = datetime.now()
        return commit and db.session.commit()

    def delete_real(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()


# ROUTING DB
class RoutingSession(orm.Session):
    def __init__(self, db, autocommit=False, autoflush=False, **options):
        self.app = db.get_app()
        self.db = db
        self._bind_name = None
        orm.Session.__init__(
            self, autocommit=autocommit, autoflush=autoflush,
            bind=db.engine,
            binds=db.get_binds(self.app),
            **options,
        )

    def get_bind(self, mapper=None, clause=None):
        try:
            state = get_state(self.app)
        except (AssertionError, AttributeError, TypeError) as err:
            current_app.logger.info(
                'cant get configuration. default bind. Error:' + err)
            return orm.Session.get_bind(self, mapper, clause)

        # If there are no binds configured, use default SQLALCHEMY_DATABASE_URI
        if not state or not self.app.config['SQLALCHEMY_BINDS']:
            return orm.Session.get_bind(self, mapper, clause)

        # if want to user exact bind
        if self._bind_name:
            # current_app.logger.info("Connecting -> SLAVE")
            return state.db.get_engine(self.app, bind=self._bind_name)
        else:
            # if no bind is used connect to default
            # current_app.logger.info("Connecting -> DEFAULT")
            return orm.Session.get_bind(self, mapper, clause)

    def using_bind(self, name):
        bind_session = RoutingSession(self.db)
        vars(bind_session).update(vars(self))
        bind_session._bind_name = name
        return bind_session


class RouteSQLAlchemy(SQLAlchemy):
    def __init__(self, *args, **kwargs):
        SQLAlchemy.__init__(self, *args, **kwargs)
        self.session.using_bind = lambda s: self.session().using_bind(s)

    def create_scoped_session(self, options=None):
        if options is None:
            options = {}
        scopefunc = options.pop('scopefunc', None)
        return orm.scoped_session(
            partial(RoutingSession, self, **options),
            scopefunc=scopefunc,
        )


cors = CORS()
db = RouteSQLAlchemy(model_class=CRUDMixin)
cache = Cache()
jwt = JWTManager()
migrate = Migrate()
ma = Marshmallow()

s3 = boto3.client(
    "s3",
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
)

# aws simple notification service
sns = boto3.client(
    "sns",
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
    region_name="us-east-1"
)

# aws simple email service
ses = boto3.client(
    "ses",
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
    region_name="us-east-1"
)
