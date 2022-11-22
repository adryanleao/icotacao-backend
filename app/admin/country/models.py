from app import db
from app.services.sqlalchemy.models import BaseModel


class Country(db.Model, BaseModel):
    __tablename__ = 'country'

    name_global = db.Column(db.String(256))
    name = db.Column(db.String(256), nullable=False)
    code = db.Column(db.String(45), nullable=False)
    code_alpha2 = db.Column(db.String(2), nullable=False)
    code_alpha3 = db.Column(db.String(3), nullable=False)
    status = db.Column(db.Integer(), nullable=False, default=1)

    def create_item(self, json):
        self.name = json['name']
        self.code = json['code']
        self.code_alpha2 = json['code_alpha2']
        self.code_alpha3 = json['code_alpha3']
        return self

    def update_item(self, json):
        self.name = json.get('name', self.name)
        self.code = json.get('code', self.code)
        self.code_alpha2 = json.get('code_alpha2', self.code_alpha2)
        self.code_alpha3 = json.get('code_alpha3', self.code_alpha3)
        self.status = json.get('status', self.status)
        return self
