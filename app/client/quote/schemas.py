from marshmallow import Schema, fields

from app.admin.company.schemas import CompanySchema
from app.admin.user.schemas import UserSchema
from app.services.sqlalchemy.schemas import AddressSchema


class QuoteProductSchema(Schema):
    class Meta:
        # Fields to expose
        fields = (
            "id", "name", "manufacturer", "observation", "quantity", "product_hash"
        )
        ordered = True


class QuoteProposalProductSchema(Schema):
    class Meta:
        # Fields to expose
        fields = (
            "id", "price", "price_real", "dont_have", "dont_stock", "quote_proposal_id", "quote_product_id",
            "name", "observation", "manufacturer", "quantity", "product_hash"
        )
        ordered = True


class QuoteProposalSchema(Schema):
    class Meta:
        # Fields to expose
        fields = (
            "id", "price", "observation", "proposal_type", "status", "products", "delivery_price",
            "shipping_included", "company", "quote_id"
        )
        ordered = True

    company = fields.Nested(CompanySchema)
    products = fields.Nested(QuoteProposalProductSchema(many=True))


class QuoteSchema(Schema):
    class Meta:
        # Fields to expose
        fields = (
            "id", "name", "proposals_deadline", "delivery_deadline", "observation",
            "payment_type", "status", "user", "created_at", "proposals", "products", "quote_hash",
            "count_proposals", "chosen", "address", "is_proposal_expired"
        )
        ordered = True

    products = fields.Nested(QuoteProductSchema(many=True))
    chosen = fields.Nested(QuoteProposalSchema)
    user = fields.Nested(UserSchema(exclude={"company", "group"}))
    address = fields.Nested(AddressSchema)
