from app.client.quote.models import QuoteProduct
from app.client.quote.schemas import QuoteProductSchema
from app.services.errors.exceptions import NotFoundError


def get_quote_product(id, schema=None, columns=None):
    query = QuoteProduct.query
    if columns:
        query = query.with_entities(*[getattr(QuoteProduct, column) for column in columns])
    item = query.filter(QuoteProduct.id == id).first()
    if not item:
        raise NotFoundError()
    if schema:
        item = QuoteProductSchema().dump(item)
    return item


def gets_quote_product(quote_id):
    return QuoteProduct.query.filter(QuoteProduct.quote_id == quote_id).all()


def create_quote_products(quote, products):
    products_return = []
    for product in products:
        product["quote_id"] = quote.id
        product["segment_id"] = quote.segment_id
        products_return.append(QuoteProduct().create_item(product).save())

    return products_return


def update_quote_products(quote_id, products):
    # get products in db from dict_body
    products_verify = []
    for product in products:
        if "id" in product:
            products_verify.append(product["id"])

    # delete products where not in dict_body
    products_delete = QuoteProduct.query.filter(QuoteProduct.id.notin_(products_verify),
                                                QuoteProduct.quote_id == quote_id).all()
    for product_delete in products_delete:
        product_delete.delete_real()

    products_return = []
    for product in products:
        if "id" in product:
            quote_product = get_quote_product(product["id"])
            products_return.append(quote_product.update_item(product).update())
        else:
            product["quote_id"] = quote_id
            products_return.append(QuoteProduct().create_item(product).save())

    return products_return
