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

    def count_user(self):
        cur = self.connection.cursor()
        cur.execute('SELECT COUNT(*) FROM LMUSER')
        count = cur.fetchone()[0]
        return count

    def test_insert_user(self):
        with DataAccess(self.connection) as dao:
            count = self.count_user()
            dao.insert_user('user1', 'Jane Doe', 'abc123')
            new_count = self.count_user()
            self.assertTrue(count + 1 == new_count)

    def test_check_if_user_exists_false(self):
        with DataAccess(self.connection) as dao:
            username = 'test'
            self.assertFalse(dao.check_if_user_exists(username))

    def test_check_if_user_exists_true(self):
        with DataAccess(self.connection) as dao:
            username = 'test'
            fullname = 'tester'
            password = 'pwd'
            dao.insert_user(username, fullname, password)
            self.assertTrue(dao.check_if_user_exists(username))


if __name__ == '__main__':
    unittest.main()
