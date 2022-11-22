from app import db
from app.services.sqlalchemy.models import BaseModel


class Segment(db.Model, BaseModel):
    __tablename__ = "segment"

    name = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(256))
    status = db.Column(db.Boolean, nullable=False, default=1)

    def create_item(self, dict_body):
        self.name = dict_body["name"]
        self.description = dict_body.get("description", None)
        self.status = dict_body.get("status", self.status)

        return self

    def update_item(self, dict_body):
        self.name = dict_body.get("name", self.name)
        self.description = dict_body.get("description", self.description)
        self.status = dict_body.get("status", self.status)

        return self
