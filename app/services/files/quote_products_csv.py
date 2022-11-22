import csv
import os

from flask import request
from werkzeug.utils import secure_filename

from app.client.quote.models import QuoteProduct
from app.client.quote.services.crud import get_quote
from app.services.files.xlsx_to_csv import csv_from_excel


def quote_products_csv():
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
                products_dict["name"] = row[0]
            except:
                products_dict["name"] = None
            try:
                products_dict["manufacturer"] = row[1]
            except:
                products_dict["manufacturer"] = None
            try:
                products_dict["observation"] = row[2]
            except:
                products_dict["observation"] = None
            try:
                products_dict["quantity"] = int(float(row[3]))
            except:
                products_dict["quantity"] = 1

            dict_return["products"].append(products_dict)
        row_num = row_num + 1

    os.remove(f'{get_dir}/{file}')
    os.remove(xlsx_file)

    return dict_return
