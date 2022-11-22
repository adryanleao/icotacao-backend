from marshmallow import Schema, fields

from app.services.sqlalchemy.schemas import AddressSchema


class CostumerSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "name", "cell_phone", "email", "tax_payer", "address")
        ordered = True

    address = fields.Nested(AddressSchema)
