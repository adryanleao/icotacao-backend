from app import db
from app.admin.city.models import City
from app.services.sqlalchemy.models import BaseModel


class Costumer(db.Model, BaseModel):
    __tablename__ = 'costumer'

    name = db.Column(db.String(256))
    cell_phone = db.Column(db.String(256))
    email = db.Column(db.String(100), nullable=False)
    tax_payer = db.Column(db.String(256), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    address = db.relationship("CostumerAddress", uselist=False, backref="costumer")

    def create_item(self, dict_body):
        self.user_id = dict_body['user_id']
        self.name = dict_body.get('name', self.name)
        self.cell_phone = dict_body.get('cell_phone', self.cell_phone)
        self.email = dict_body.get('email', self.email)
        self.tax_payer = dict_body.get('tax_payer', self.tax_payer)

        return self

    def update_item(self, dict_body):
        self.name = dict_body.get('name', self.name)
        self.cell_phone = dict_body.get('cell_phone', self.cell_phone)
        self.email = dict_body.get('email', self.email)
        self.tax_payer = dict_body.get('tax_payer', self.tax_payer)

        return self


class CostumerAddress(db.Model, BaseModel):
    __tablename__ = "costumer_address"

    code_post = db.Column(db.String(256))
    street = db.Column(db.String(256))
    number = db.Column(db.String(256))
    district = db.Column(db.String(256))
    complement = db.Column(db.String(256))

    city_id = db.Column(db.Integer, db.ForeignKey("city.id"))
    costumer_id = db.Column(db.Integer, db.ForeignKey("costumer.id"))

    city = db.relationship(City, uselist=False, backref="costumer_address")

    def create_item(self, dict_body):
        self.code_post = dict_body["code_post"]
        self.street = dict_body["street"]
        self.number = dict_body["number"]
        self.district = dict_body["district"]
        self.complement = dict_body["complement"]
        self.costumer_id = dict_body["costumer_id"]
        self.city_id = dict_body["city"]["id"]

        return self

    def update_item(self, dict_body):
        self.code_post = dict_body["code_post"]
        self.street = dict_body["street"]
        self.number = dict_body["number"]
        self.district = dict_body["district"]
        self.complement = dict_body["complement"]
        self.city_id = dict_body["city"]["id"]

        return self
