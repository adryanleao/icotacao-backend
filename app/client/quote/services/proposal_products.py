from app.client.quote.models import QuoteProposalProduct, QuoteProduct
from app.client.quote.schemas import QuoteProposalProductSchema
from app.client.quote.services.products import get_quote_product
from app.services.errors.exceptions import NotFoundError


def get_proposal_product(id, proposal_id, schema=None, columns=None):
    query = QuoteProposalProduct.query
    if columns:
        query = query.with_entities(*[getattr(QuoteProposalProduct, column) for column in columns])
    item = query.filter(QuoteProposalProduct.quote_product_id == id, 
                        QuoteProposalProduct.quote_proposal_id == proposal_id).first()
    if not item:
        raise NotFoundError()
    if schema:
        item = QuoteProposalProductSchema().dump(item)
    return item


def gets_proposal_product(proposal_id):
    return QuoteProposalProduct.query.filter(QuoteProposalProduct.quote_proposal_id == proposal_id).all()


def create_proposal_products(proposal, products):
    total = 0.0
    for product in products:
        quote_product = QuoteProduct.query.filter(QuoteProduct.id == product["id"],
                                                  QuoteProduct.quote_id == proposal.quote_id).first()
        if not quote_product:
            raise NotFoundError(f"Product ID: {product['id']} not found")

        product_dict = {
            "quote_proposal_id": proposal.id,
            "quote_product_id": quote_product.id
        }
        if "price" in product:
            product_dict["price"] = product["price"]
        else:
            product_dict["price"] = 0
        if "dont_have" in product:
            product_dict["dont_have"] = product["dont_have"]
        if "dont_stock" in product:
            product_dict["dont_stock"] = product["dont_stock"]
        created_product = QuoteProposalProduct().create_item(product_dict).save()

        product_price = created_product.price if created_product.dont_have == False else 0
        if created_product.dont_have == False and created_product.dont_stock == False:
            product_price = created_product.price
        else:
            product_price = 0

        total += (quote_product.quantity * product_price) + proposal.price

    if proposal.shipping_included == 1:
        proposal.price = total + proposal.delivery_price
    else:
        proposal.price = total
    proposal.update()

    return True


def update_proposal_products(proposal, products):
    products_return = []
    for product in products:
        quote_product = QuoteProduct.query.filter(QuoteProduct.id == product["id"],
                                                  QuoteProduct.quote_id == proposal.quote_id).first()
        if not quote_product:
            raise NotFoundError(f"Product ID: {product['id']} not found")
        try:
            proposal_product = get_proposal_product(product["id"], proposal.id)
            products_return.append(proposal_product.update_item(product).update())
        except:
            product["quote_proposal_id"] = proposal.id
            product["quote_product_id"] = quote_product.id
            products_return.append(QuoteProposalProduct().create_item(product).save())

    total = 0
    for product in products_return:
        total = total + (product.price * product.product.quantity)
    proposal.price = total + proposal.delivery_price
    proposal.update()

    return products_return
