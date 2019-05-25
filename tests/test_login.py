import unittest
from rp_app.login_with_password import LoginWithPassword


class TestLogin(unittest.TestCase):

    def setUp(self):
        self.login_with_password = LoginWithPassword(ip_dict={'ip': 'test'})

    def test_login_with_wrong_username(self):
        self.login_with_password._LoginWithPassword__password = 'abc123'
        self.login_with_password._LoginWithPassword__username = 'youtube'
        self.assertFalse(self.login_with_password.login_with_password())

    def test_login_with_wrong_password(self):
        self.login_with_password._LoginWithPassword__password = 'abcdefg'
        self.login_with_password._LoginWithPassword__username = 'flydog'
        self.assertFalse(self.login_with_password.login_with_password())


if __name__ == '__main__':
    unittest.main()
