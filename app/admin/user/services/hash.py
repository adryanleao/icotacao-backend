from cryptography.fernet import Fernet

from config import Config


def encrypt_user_id(user_id):
    key = Config.KEY_CRYPTOGRAPHY
    user_id_crypt = Fernet(key).encrypt(str(user_id).encode())
    return user_id_crypt.decode()


def decrypt_user_id(token):
    key = Config.KEY_CRYPTOGRAPHY
    user_id_decrypt = Fernet(key).decrypt(token.encode())
    return user_id_decrypt.decode()
