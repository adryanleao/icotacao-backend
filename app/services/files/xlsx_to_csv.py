import csv

import xlrd


def csv_from_excel(file_dir, file):
    wb = xlrd.open_workbook(f'{file_dir}/{file}')
    sh = wb.sheet_by_name('Sheet1')
    csv_file = open(f'{file_dir}/products.csv', 'w')
    wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    csv_file.close()

    return csv_file.name