import csv
import os

from flask import request
from werkzeug.utils import secure_filename

from app.client.quote.models import QuoteProduct
from app.client.quote.services.crud import get_quote
from app.services.errors.exceptions import NotFoundError
from app.services.files.xlsx_to_csv import csv_from_excel


def proposal_products_csv():
    get_dir = f'{os.getcwd()}/tmp'
    file_request = request.files["file"]
    file = secure_filename(file_request.filename)

    if os.path.exists(f'{get_dir}'):
        pass
    else:
        os.mkdir(f'{get_dir}')
    with open(f'{get_dir}/{file}', 'wb') as f:
        f.write(file_request.read())

    xlsx_file = csv_from_excel(get_dir, file)
    csv_data = csv.reader(open(xlsx_file))

    row_num = 0
    dict_return = {"products": []}
    for row in csv_data:
        if row_num > 0:
            products_dict = {}
            try:
                product = QuoteProduct.query.filter(QuoteProduct.product_hash == str(row[0])).first()
                products_dict["id"] = product.id
            except:
                raise NotFoundError("Verifique o arquivo e tente novamente!")
            try:
                products_dict["price"] = float(row[2])
            except:
                products_dict["price"] = None
            try:
                if row[3] in ("Não", "não", "NÃO", "n", "N"):
                    products_dict["dont_have"] = 1
                else:
                    products_dict["dont_have"] = 0
            except:
                products_dict["dont_have"] = 0
            try:
                if row[4] in ("Não", "não", "NÃO", "n", "N"):
                    products_dict["dont_stock"] = 1
                else:
                    products_dict["dont_stock"] = 0
            except:
                products_dict["dont_stock"] = 0

            dict_return["products"].append(products_dict)
        row_num = row_num + 1

    os.remove(f'{get_dir}/{file}')
    os.remove(xlsx_file)

    return dict_return
