from datetime import datetime
from flask_sqlalchemy import Model
from sqlalchemy import Column, Integer, DateTime

from app.services.utils.utils import get_now


class BaseModel(Model):
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    created_at = Column(DateTime, default=get_now)
    updated_at = Column(DateTime, default=get_now, onupdate=get_now)
    deleted_at = Column(DateTime)

    @classmethod
    def get_by_id(cls, record_id):
        return cls.query.get(int(record_id))
