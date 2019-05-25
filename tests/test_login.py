import unittest
from unittest import mock
from rp_app.user_login import UserLogin
from rp_app.login_with_password import LoginWithPassword


class TestLogin(unittest.TestCase):

    def setUp(self):
        self.user_login = UserLogin()
        self.login_with_password = LoginWithPassword

    def test_login_with_wrong_username(self):
        self.login_with_password._LoginWithPassword__password = mock(return_value='abc123')
        self.login_with_password._LoginWithPassword__username = mock(return_value='youtube')
        self.assertFalse(self.login_with_password.login_with_password(), False)

    def test_login_with_wrong_password(self):
        self.login_with_password._LoginWithPassword__password = mock(return_value='abcdefg')
        self.login_with_password._LoginWithPassword__username = mock(return_value='flydog')
        self.assertFalse(self.login_with_password.login_with_password(), False)


if __name__ == '__main__':
    unittest.main()
