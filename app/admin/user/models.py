import uuid
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from app import db
from app.admin.city.models import City
from app.services.aws.s3 import get_aws_image_keys_private
from app.services.codes.generation import get_promo_code
from app.services.sqlalchemy.models import BaseModel

"""
Credential levels

1 - System / Sistema (Desenvolvedores)
2 - Admin (Contratante)
3 - Editor
4 - Fornecedor 
5 - Client / Cliente (usuários da plataforma)
"""


class User(db.Model, BaseModel):
    __tablename__ = "user"

    email = db.Column(db.String(100), nullable=False)
    email_verified = db.Column(db.Integer, default=0)
    token_update = db.Column(db.String(36))
    password = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(256), nullable=False)
    image_key = db.Column(db.String(256))
    cpf = db.Column(db.String(256))
    description = db.Column(db.String(256))
    cell_phone = db.Column(db.String(256))
    status = db.Column(db.Boolean, default=1)
    code_promo = db.Column(db.String(50))
    code_partner = db.Column(db.String(50))
    receive_quotes = db.Column(db.Boolean, nullable=False, default=0)

    # ForeignKeys
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"))
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    group = db.relationship('Group', backref='user', lazy=True, uselist=False)
    company = db.relationship('Company', backref='user', lazy=True, uselist=False)
    address = db.relationship("UserAddress", uselist=False, backref="user")

    def _get_image(self):
        return get_aws_image_keys_private(self.image_key)

    image = property(_get_image)

    def set_password(self, password):
        self.password = pbkdf2_sha256.hash(password)[20:]

    def check_password(self, candidate):
        return pbkdf2_sha256.verify(candidate, f"$pbkdf2-sha256$29000{self.password}")

    def create_item(self, dict_body):
        self.code_promo = f"US{get_promo_code(6)}"
        self.email = dict_body.get("email", self.email)
        self.set_password(dict_body["password"])
        self.token_update = str(uuid.uuid4())
        self.name = dict_body.get("name", self.name)
        self.cpf = dict_body.get("cpf", self.cpf)
        self.description = dict_body.get("description", self.description)
        self.cell_phone = dict_body.get("cell_phone", self.cell_phone)
        self.code_partner = dict_body.get("code_partner", self.code_partner)
        self.company_id = dict_body.get("company_id", self.company_id)
        self.receive_quotes = dict_body.get("receive_quotes", self.receive_quotes)
        try:
            self.group_id = dict_body["group_id"]
        except:
            try:
                self.group_id = dict_body["group"]["id"]
            except:
                self.group_id = 5

        return self

    def update_item(self, dict_body):
        try:
            self.set_password(dict_body["password"])
        except:
            pass
        self.name = dict_body.get("name", self.name)
        self.cpf = dict_body.get("cpf", self.cpf)
        self.description = dict_body.get("description", self.description)
        self.cell_phone = dict_body.get("cell_phone", self.cell_phone)
        self.status = dict_body.get("status", self.status)
        self.receive_quotes = dict_body.get("receive_quotes", self.receive_quotes)
        return self


class UserAddress(db.Model, BaseModel):
    __tablename__ = "user_address"

    code_post = db.Column(db.String(256))
    street = db.Column(db.String(256))
    number = db.Column(db.String(256))
    district = db.Column(db.String(256))
    complement = db.Column(db.String(256))

    lat = db.Column(db.String(256))
    long = db.Column(db.String(256))

    city_id = db.Column(db.Integer, db.ForeignKey("city.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    city = db.relationship(City, uselist=False, backref="user_address")

    def create_item(self, dict_body):
        self.code_post = dict_body["code_post"]
        self.street = dict_body["street"]
        self.number = dict_body["number"]
        self.district = dict_body["district"]
        self.complement = dict_body["complement"]
        self.lat = dict_body.get("lat", None)
        self.long = dict_body.get("long", None)
        self.user_id = dict_body["user_id"]
        self.city_id = dict_body["city"]["id"]

        return self

    def update_item(self, dict_body):
        self.code_post = dict_body["code_post"]
        self.street = dict_body["street"]
        self.number = dict_body["number"]
        self.district = dict_body["district"]
        self.complement = dict_body["complement"]
        self.lat = dict_body.get("lat", self.lat)
        self.long = dict_body.get("long", self.long)
        self.city_id = dict_body["city"]["id"]

        return self
