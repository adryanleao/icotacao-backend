import uuid

import pytz
from sqlalchemy import func

from app import db
from app.admin.city.models import City
from app.admin.company.models import Company
from app.admin.user.models import User
from app.services.sqlalchemy.models import BaseModel
from app.services.utils.utils import float_to_real_money, get_now

"""
Status
0 = Rascunho
1 = Enviado
2 = Concluído
3 = Cancelado

Payment type
1 = Dinheiro
2 = Boleto
3 = Transferência Ted
4 = Cartão de Crédito
5 = Cartão de Débito
6 = PIX
"""


class Quote(db.Model, BaseModel):
    __tablename__ = "quote"

    name = db.Column(db.String(256), nullable=False)
    quote_hash = db.Column(db.String(6))
    proposals_deadline = db.Column(db.DateTime)
    delivery_deadline = db.Column(db.DateTime)
    observation = db.Column(db.Text)
    payment_type = db.Column(db.Integer)
    status = db.Column(db.Integer, nullable=False, default=1)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    costumer_id = db.Column(db.Integer, db.ForeignKey("costumer.id"))
    segment_id = db.Column(db.Integer, db.ForeignKey("segment.id"))

    address = db.relationship("QuoteAddress", uselist=False, backref="quote")

    def _get_products(self):
        return QuoteProduct.query.filter(QuoteProduct.quote_id == self.id).all()

    products = property(_get_products)

    def _get_user(self):
        return User.query \
            .filter(User.id == self.user_id, User.deleted_at == None) \
            .first()

    user = property(_get_user)

    def _get_chosen(self):
        return QuoteProposal.query \
            .filter(QuoteProposal.quote_id == self.id, QuoteProposal.status == 2, QuoteProposal.deleted_at == None) \
            .first()

    chosen = property(_get_chosen)

    def _count_proposals(self):
        item = QuoteProposal.query.with_entities(func.count(QuoteProposal.id).label('total_count')) \
            .filter(QuoteProposal.quote_id == self.id).first()

        return int(item.total_count)

    count_proposals = property(_count_proposals)

    def _is_proposal_expired(self):
        if self.proposals_deadline.replace(tzinfo=pytz.timezone("America/Sao_Paulo")) <= get_now():
            return True
        return False

    is_proposal_expired = property(_is_proposal_expired)

    def create_item(self, dict_body):
        self.user_id = dict_body["user_id"]
        self.quote_hash = str(uuid.uuid1())
        self.costumer_id = dict_body.get("costumer_id", None)
        self.segment_id = dict_body.get("segment_id", self.segment_id)
        self.name = dict_body["name"]
        self.proposals_deadline = dict_body["proposals_deadline"]
        self.delivery_deadline = dict_body["delivery_deadline"]
        self.observation = dict_body.get("observation", self.observation)
        self.payment_type = dict_body.get("payment_type", self.payment_type)
        self.status = dict_body.get("status", 0)

        return self

    def update_item(self, dict_body):
        self.name = dict_body.get("name", self.name)
        self.costumer_id = dict_body.get("costumer_id", self.costumer_id)
        self.segment_id = dict_body.get("segment_id", self.segment_id)
        self.proposals_deadline = dict_body.get("proposals_deadline", self.proposals_deadline)
        self.delivery_deadline = dict_body.get("delivery_deadline", self.delivery_deadline)
        self.observation = dict_body.get("observation", self.observation)
        self.payment_type = dict_body.get("payment_type", self.payment_type)
        self.status = dict_body.get("status", self.status)

        return self


class QuoteProduct(db.Model, BaseModel):
    __tablename__ = "quote_product"

    name = db.Column(db.String(256), nullable=False)
    manufacturer = db.Column(db.String(256))
    observation = db.Column(db.Text)
    quantity = db.Column(db.Integer)
    product_hash = db.Column(db.String(6))

    quote_id = db.Column(db.Integer, db.ForeignKey("quote.id"))
    segment_id = db.Column(db.Integer, db.ForeignKey("segment.id"))

    def create_item(self, dict_body):
        self.quote_id = dict_body["quote_id"]
        self.segment_id = dict_body.get("segment_id", self.segment_id)
        self.name = dict_body["name"]
        self.manufacturer = dict_body["manufacturer"]
        self.observation = dict_body.get("observation", self.observation)
        self.quantity = dict_body.get("quantity", 1)
        self.product_hash = str(uuid.uuid1())

        return self

    def update_item(self, dict_body):
        self.segment_id = dict_body.get("segment_id", self.segment_id)
        self.name = dict_body.get("name", self.name)
        self.manufacturer = dict_body.get("manufacturer", self.manufacturer)
        self.observation = dict_body.get("observation", self.observation)
        self.quantity = dict_body.get("quantity", 1)

        return self


class QuoteProposal(db.Model, BaseModel):
    __tablename__ = "quote_proposal"

    price = db.Column(db.Float)
    delivery_price = db.Column(db.Float)
    shipping_included = db.Column(db.Boolean, nullable=False, default=0)
    observation = db.Column(db.Text)
    status = db.Column(db.Integer, nullable=False, default=1)

    quote_id = db.Column(db.Integer, db.ForeignKey("quote.id"))
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))

    def _get_products(self):
        products = db.session.using_bind("slave") \
            .query(QuoteProposalProduct) \
            .filter(QuoteProposalProduct.quote_proposal_id == self.id, QuoteProposalProduct.deleted_at == None) \
            .all()
        for product in products:
            quote_product = QuoteProduct.query.filter(QuoteProduct.id == product.quote_product_id).first()
            product.price_real = float_to_real_money(product.price)
            product.name = quote_product.name
            product.product_hash = quote_product.product_hash
            product.quantity = quote_product.quantity
            product.observation = quote_product.observation
            product.manufacturer = quote_product.manufacturer

        return products

    products = property(_get_products)

    def _get_company(self):
        return Company.query.filter(Company.id == self.company_id, Company.deleted_at == None).first()

    company = property(_get_company)

    def create_item(self, dict_body):
        self.quote_id = dict_body["quote_id"]
        self.company_id = dict_body["company_id"]
        self.observation = dict_body.get("observation", self.observation)
        self.price = dict_body.get("price", 0)
        self.delivery_price = dict_body.get("delivery_price", 0)
        self.shipping_included = dict_body.get("shipping_included", self.shipping_included)
        self.status = dict_body.get("status", self.status)

        return self

    def update_item(self, dict_body):
        self.price = dict_body.get("price", self.price)
        self.delivery_price = dict_body.get("delivery_price", self.delivery_price)
        self.observation = dict_body.get("observation", self.observation)
        self.shipping_included = dict_body.get("shipping_included", self.shipping_included)
        self.status = dict_body.get("status", self.status)

        return self


class QuoteProposalProduct(db.Model, BaseModel):
    __tablename__ = "quote_proposal_product"

    price = db.Column(db.Float)
    dont_have = db.Column(db.Boolean, nullable=False, default=0)
    dont_stock = db.Column(db.Boolean, nullable=False, default=0)

    quote_proposal_id = db.Column(db.Integer, db.ForeignKey("quote_proposal.id"))
    quote_product_id = db.Column(db.Integer, db.ForeignKey("quote_product.id"))

    def _get_product(self):
        return db.session.using_bind("slave") \
            .query(QuoteProduct) \
            .filter(QuoteProduct.id == self.quote_product_id, QuoteProduct.deleted_at == None) \
            .first()

    product = property(_get_product)

    def create_item(self, dict_body):
        self.quote_proposal_id = dict_body["quote_proposal_id"]
        self.quote_product_id = dict_body["quote_product_id"]
        self.price = dict_body.get("price", self.price)
        self.dont_have = dict_body.get("dont_have", self.dont_have)
        self.dont_stock = dict_body.get("dont_stock", self.dont_stock)

        return self

    def update_item(self, dict_body):
        self.price = dict_body.get("price", self.price)
        self.dont_have = dict_body.get("dont_have", self.dont_have)
        self.dont_stock = dict_body.get("dont_stock", self.dont_stock)

        return self


class QuoteAddress(db.Model, BaseModel):
    __tablename__ = "quote_address"

    code_post = db.Column(db.String(256))
    street = db.Column(db.String(256))
    number = db.Column(db.String(256))
    district = db.Column(db.String(256))
    complement = db.Column(db.String(256))

    city_id = db.Column(db.Integer, db.ForeignKey("city.id"))
    quote_id = db.Column(db.Integer, db.ForeignKey("quote.id"))

    city = db.relationship(City, uselist=False, backref="quote_address")

    def create_item(self, dict_body):
        self.code_post = dict_body["code_post"]
        self.street = dict_body["street"]
        self.number = dict_body["number"]
        self.district = dict_body["district"]
        self.complement = dict_body["complement"]
        self.quote_id = dict_body["quote_id"]
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
