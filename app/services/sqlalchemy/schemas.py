from marshmallow import Schema, fields

from app.admin.city.schemas import CitySchema


class ReducedSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "name", "status")
        ordered = True


class ImageSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ("original", "small", "medium", "large")
        ordered = True


class AddressSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ("code_post", "street", "number", "district", "complement", "city")
        ordered = True

    city = fields.Nested(CitySchema())
