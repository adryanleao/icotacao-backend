from marshmallow import fields

from app import ma
from app.admin.city.schemas import CitySchema
from app.admin.company.schemas import CompanySchema
from app.services.sqlalchemy.schemas import ReducedSchema


class UserAddressSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = (
            "id", "code_post", "street", "number", "district", "complement", "city")
        ordered = True

    city = fields.Nested(CitySchema)


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = (
            "id", "name", "email", "receive_quotes", "status", "cpf", "cell_phone", "image", "config", "group",
            "address", "company")
        ordered = True

    group = fields.Nested(ReducedSchema)
    company = fields.Nested(CompanySchema)
    address = fields.Nested(UserAddressSchema)
