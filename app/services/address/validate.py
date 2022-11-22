import requests
from flask import request

from app.admin.city.models import City
from app.admin.city.schemas import CitySchema
from app.admin.state.models import State
from app.services.errors.exceptions import NotFoundError


def validate_address_by_code_post():
    code_post = request.args.get('code_post')

    if code_post is None:
        raise NotFoundError('CEP não encontrado')

    header = {
        'Content-Type': 'application/json'
    }

    try:
        url = 'https://viacep.com.br/ws/{}/json/'.format(code_post)
        r = requests.get(url, headers=header)
        address = r.json()

        city_name = address['localidade']
        uf_name = address['uf']
        street = address['logradouro']
        district = address['bairro']
    except:
        try:
            url = 'http://cep.republicavirtual.com.br/web_cep.php?cep={}&formato=jsonp'.format(code_post)
            r = requests.get(url, headers=header)
            address = r.json()

            city_name = address['cidade']
            uf_name = address['uf']
            street = f"{address['tipo_logradouro']} {address['logradouro']}"
            district = address['bairro']
        except:
            url = 'http://apps.widenet.com.br/busca-cep/api/cep/{}.json'.format(code_post)
            r = requests.get(url, headers=header)
            address = r.json()

            city_name = address['city']
            uf_name = address['state']
            street = address['address']
            district = address['district']

    if uf_name == "":
        raise NotFoundError('Cidade não encontrada')

    city = City.query \
        .join(State, State.id == City.state_id) \
        .filter(City.name == city_name, State.uf == uf_name, City.deleted_at == None).first()

    return {
        "code_post": code_post,
        "street": street,
        "number": "",
        "district": district,
        "complement": '',
        "city": CitySchema().dump(city)
    }
