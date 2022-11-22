from app import db
from app.admin.city.models import City
from app.admin.segment.models import Segment
from app.services.sqlalchemy.models import BaseModel


class Company(db.Model, BaseModel):
    __tablename__ = "company"

    name = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    cell_phone = db.Column(db.String(256), nullable=False)
    cnpj = db.Column(db.String(256))
    status = db.Column(db.Boolean, nullable=False, default=1)
    receive_quotes = db.Column(db.Boolean, nullable=False, default=0)

    address = db.relationship("CompanyAddress", uselist=False, backref="company")

    def _get_segments(self):
        return db.session.using_bind("slave") \
            .query(Segment) \
            .with_entities(Segment.id, Segment.name) \
            .join(CompanySegment, CompanySegment.segment_id == Segment.id) \
            .filter(CompanySegment.company_id == self.id, Segment.deleted_at == None) \
            .all()

    segments = property(_get_segments)

    def create_item(self, dict_body):
        self.name = dict_body["name"]
        self.email = dict_body.get("email", self.email)
        self.cell_phone = dict_body.get("cell_phone", self.cell_phone)
        self.cnpj = dict_body.get("cnpj", self.cnpj)
        self.status = dict_body.get("status", self.status)
        self.receive_quotes = dict_body.get("receive_quotes", self.receive_quotes)

        self.address = CompanyAddress().create_item(dict_body["address"]).save()

        return self

    def update_item(self, dict_body):
        self.name = dict_body.get("name", self.name)
        self.email = dict_body.get("email", self.email)
        self.cell_phone = dict_body.get("cell_phone", self.cell_phone)
        self.cnpj = dict_body.get("cnpj", self.cnpj)
        self.status = dict_body.get("status", self.status)
        self.receive_quotes = dict_body.get("receive_quotes", self.receive_quotes)

        self.address.update_item(dict_body["address"]).update()
        return self


class CompanyAddress(db.Model, BaseModel):
    __tablename__ = "company_address"

    code_post = db.Column(db.String(256))
    street = db.Column(db.String(256))
    number = db.Column(db.String(256))
    district = db.Column(db.String(256))
    complement = db.Column(db.String(256))

    lat = db.Column(db.String(256))
    long = db.Column(db.String(256))

    city_id = db.Column(db.Integer, db.ForeignKey("city.id"))
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))

    city = db.relationship(City, uselist=False, backref="company_address")

    def create_item(self, dict_body):
        self.code_post = dict_body["code_post"]
        self.street = dict_body["street"]
        self.number = dict_body["number"]
        self.district = dict_body["district"]
        self.complement = dict_body["complement"]
        self.lat = dict_body.get("lat", None)
        self.long = dict_body.get("long", None)
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


class CompanySegment(db.Model, BaseModel):
    __tablename__ = "company_segment"

    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    segment_id = db.Column(db.Integer, db.ForeignKey("segment.id"))

    def create_item(self, dict_body):
        self.company_id = dict_body["company_id"]
        self.segment_id = dict_body["segment_id"]

        return self
