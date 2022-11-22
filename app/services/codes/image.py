import base64
from mimetypes import guess_extension, guess_type


def get_base64_image(file):
    file_exp = file.split(',')
    image = base64.b64decode(file_exp[1])
    ext = guess_extension(guess_type(file)[0])

    return image, ext
