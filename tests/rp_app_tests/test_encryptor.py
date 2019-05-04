import unittest
from rp_app.encryptor import Encryptor


class TestEncryptor(unittest.TestCase):

    def test_verify_true(self):
        password = 'abc123!'
        encrypted_password = Encryptor.encrypt(password)
        self.assertTrue(Encryptor.verify(password, encrypted_password))

    def test_verify_false(self):
        password = 'abc123'
        encrypted_password = Encryptor.encrypt(password)
        wrong_password = 'abc124'
        self.assertFalse(Encryptor.verify(wrong_password, encrypted_password))
