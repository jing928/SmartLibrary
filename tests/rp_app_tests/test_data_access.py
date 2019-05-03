import unittest
from rp_app.data_access_local import DataAccess


class TestDataAccess(unittest.TestCase):

    def test_check_if_user_exists_false(self):
        dao = DataAccess(in_memory=True)
        username = 'test'
        self.assertFalse(dao.check_if_user_exists(username))

    def test_check_if_user_exists_true(self):
        dao = DataAccess(in_memory=True)
        username = 'test'
        fullname = 'tester'
        password = 'pwd'
        dao.insert_user(username, fullname, password)
        self.assertTrue(dao.check_if_user_exists(username))


if __name__ == '__main__':
    unittest.main()
