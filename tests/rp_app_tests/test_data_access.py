import unittest
import sqlite3 as lite
from rp_app.data_access_local import DataAccess


class TestDataAccess(unittest.TestCase):

    def setUp(self):
        self.connection = lite.connect(':memory:',
                                       detect_types=lite.PARSE_DECLTYPES | lite.PARSE_COLNAMES)

    def tearDown(self):
        self.connection.close()
        self.connection = None

    def test_check_if_user_exists_false(self):
        dao = DataAccess(self.connection)
        username = 'test'
        self.assertFalse(dao.check_if_user_exists(username))

    def test_check_if_user_exists_true(self):
        dao = DataAccess(self.connection)
        username = 'test'
        fullname = 'tester'
        password = 'pwd'
        dao.insert_user(username, fullname, password)
        self.assertTrue(dao.check_if_user_exists(username))


if __name__ == '__main__':
    unittest.main()
