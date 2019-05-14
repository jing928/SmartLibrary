"""
This module has the Encryptor class to provide hash and salt functions to passwords.
"""

import hashlib
import os
import binascii


class Encryptor:
    """
    The Encryptor class provides static functions to encrypt and verify passwords.

    The code is adapted from https://www.vitoshacademy.com/hashing-passwords-in-python/
    """

    @staticmethod
    def encrypt(password):
        """ Encrypt a plain password string using hash and salt.

        It creates a random salt using SHA-256 method and then creates a hash of
        the plain password plus the salt.

        Args:
            password: the plain string of the password.

        Returns:
            str: A string of hash value of the password with the salt prefixed.

        """
        salt = hashlib.sha256(os.urandom(16)).hexdigest()
        string_hash = Encryptor.__hash_string_with_salt(password, salt)
        return salt + string_hash

    @staticmethod
    def verify(password_plain, password_hash_and_salt):
        """Verifies if the plain password matches the hashed password.

        It first extracts the salt from the hashed password and then uses the same
        method to generate a hash with the salt and the plain password. Lastly it
        compares the newly generated hash with hashed password.

        Args:
            password_plain: a plain password string to be verified.
            password_hash_and_salt: the saved hash value of the correct password.

        Returns:
            bool: True if the plain password matches the saved password, False otherwise.

        """
        salt = password_hash_and_salt[:64]
        password_hash = password_hash_and_salt[64:]
        new_password_hash = Encryptor.__hash_string_with_salt(password_plain, salt)
        return password_hash == new_password_hash

    @staticmethod
    def __hash_string_with_salt(string, salt):
        """A helper method to generate the hash value of password plus salt.

        It uses SHA-256 method to hash the plain password and the salt together.

        Args:
            string: the plain password string.
            salt: a random string.

        Returns:
            str: string representation of the hash value of the password and salt.

        """
        hash_bytes = hashlib.pbkdf2_hmac('sha256', string.encode('utf-8'),
                                         salt.encode('ascii'), 100000)
        return binascii.hexlify(hash_bytes).decode('ascii')
