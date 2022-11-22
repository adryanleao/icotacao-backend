from marshmallow import Schema, fields

from app.admin.segment.schemas import SegmentSchema
from app.services.sqlalchemy.schemas import AddressSchema


class CompanySchema(Schema):
    class Meta:
        # Fields to expose
        fields = (
            "id", "receive_quotes", "name", "email", "cell_phone", "cnpj", "password", "status", "segments", "address",
        )
        ordered = True

    segments = fields.Nested(SegmentSchema(many=True))
    address = fields.Nested(AddressSchema)


class CompanySegmentSchema(Schema):
    class Meta:
        # Fields to expose
        fields = (
            "id", "company_id", "segment_id"
        )
        ordered = True
