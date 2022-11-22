from marshmallow import fields

from app import ma
from app.client.quote.schemas import QuoteSchema


class NotificationSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "name", "icon", "description", "quote", "status")
        ordered = True

    quote = fields.Nested(QuoteSchema)
