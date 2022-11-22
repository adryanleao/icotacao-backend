import datetime

import pytz


def float_to_real_money(value):
    a = '{:,.2f}'.format(float(value))
    b = a.replace(',', 'v')
    c = b.replace('.', ',')
    return c.replace('v', '.')


def get_now(t=None, utc="America/Sao_Paulo"):
    timezone = pytz.timezone(utc)

    if t == "year":
        now = datetime.datetime.now(tz=timezone).year

    elif t == "month":
        now = datetime.datetime.now(tz=timezone).month

    elif t == "day":
        now = datetime.datetime.now(tz=timezone).day

    else:
        now = datetime.datetime.now(tz=timezone)

    return now
