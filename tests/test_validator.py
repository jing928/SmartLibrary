import unittest
from utils.validator import Validator


class TestValidator(unittest.TestCase):
    def test_validate_username_with_valid_input(self):
        valid_input = 'tester1'
        result = Validator.validate_username(valid_input)
        self.assertTrue(result)

    def test_validate_username_with_invalid_input(self):
        invalid_input = ';delete all'
        result = Validator.validate_username(invalid_input)
        self.assertFalse(result)

    def test_validate_fullname_with_valid_input(self):
        valid_input = 'John Doe'
        result = Validator.validate_fullname(valid_input)
        self.assertTrue(result)

    def test_validate_fullname_with_invalid_input(self):
        invalid_input = '123'
        result = Validator.validate_fullname(invalid_input)
        self.assertFalse(result)

    def test_validate_password_with_valid_input(self):
        valid_input = 'abc123'
        result = Validator.validate_password(valid_input)
        self.assertTrue(result)

    def test_validate_password_with_invalid_input(self):
        invalid_input = '123456'
        result = Validator.validate_password(invalid_input)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
