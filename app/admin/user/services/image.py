import uuid
from flask import request

from app.services.aws.s3 import delete_file_s3, get_aws_image_keys_private, upload_file_s3
from app.services.codes.image import get_base64_image


def create_user_image(item):
    dict_body = request.get_json()
    image, ext = get_base64_image(dict_body['image'])
    upload = upload_file_s3(image, f'images/users/{item.id}', f'{str(uuid.uuid1())}{ext}')

    try:
        delete_file_s3(item.image_key)
    except:
        pass

    try:
        image_key = upload['image_key']
        item.image_key = image_key
        item.update()
    except:
        image_key = item.image_key
        pass

    image_return = get_aws_image_keys_private(image_key)

    return image_return
