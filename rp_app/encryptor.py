import hashlib
import os
import binascii


class Encryptor:

    @staticmethod
    def encrypt(password):
        salt = hashlib.sha256(os.urandom(16)).hexdigest()
        string_hash = Encryptor.__hash_string_with_salt(password, salt)
        return salt + string_hash

    @staticmethod
    def verify(password_plain, password_hash_and_salt):
        salt = password_hash_and_salt[:64]
        password_hash = password_hash_and_salt[64:]
        new_password_hash = Encryptor.__hash_string_with_salt(password_plain, salt)
        return password_hash == new_password_hash

    @staticmethod
    def __hash_string_with_salt(string, salt):
        hash_bytes = hashlib.pbkdf2_hmac('sha256', string.encode('utf-8'),
                                         salt.encode('ascii'), 100000)
        return binascii.hexlify(hash_bytes).decode('ascii')
