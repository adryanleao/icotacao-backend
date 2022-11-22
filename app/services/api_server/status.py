def code_message(message_or_code):
    if message_or_code == 1:
        message = "Cadastrado com Sucesso"
    elif message_or_code == 2:
        message = "Consulta Realizada com Sucesso"
    elif message_or_code == 3:
        message = "Atualizado com Sucesso"
    elif message_or_code == 4:
        message = "Deletado com Sucesso"
    elif message_or_code == 5:
        message = "Está faltando um campo"
    elif message_or_code == 6:
        message = "Não Encontrado"
    elif message_or_code == 7:
        message = "Item já Cadastrado"
    elif message_or_code == 8:
        message = "Item já Deletado"
    elif message_or_code == 9:
        message = "Fluxo de alteração de status não permitido. Os dados não foram atualizados"
    else:
        message = message_or_code

    return message


def code_http(code):
    if code == 200:
        status = "OK"
    if code == 201:
        status = "Created"
    if code == 204:
        status = "No Content"
    if code == 206:
        status = "Partial Content"
    if code == 302:
        status = "Found"
    if code == 400:
        status = "Bad Request"
    if code == 401:
        status = "Unauthorized"
    if code == 402:
        status = "Payment Unauthorized"
    if code == 403:
        status = "Forbidden"
    if code == 404:
        status = "Not Found"
    if code == 405:
        status = "Method Not Allowed"
    if code == 406:
        status = "Not Acceptable"
    if code == 409:
        status = "Conflict"
    if code == 415:
        status = "Unsupported Media Type"
    if code == 429:
        status = "Too Many Request"
    if code == 500:
        status = "Internal Server Error"
    if code == 503:
        status = "Service Unavailable"

    return status
