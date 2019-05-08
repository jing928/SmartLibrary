import pymysql as mysql
from utils.file_access import FileAccess


class DataAccessCloud():

    def __init__(self, connection=None):
        if connection is None:
            db_config = FileAccess.get_db_config()
            connection = mysql.connect(host=db_config['HOST'],
                                       user=db_config['USER'],
                                       password=db_config['PASSWORD'],
                                       db=db_config['DATABASE'],
                                       charset='utf8mb4',
                                       cursorclass=mysql.cursors.DictCursor)
        self.con = connection

    def close(self):
        self.con.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

    def search(self, query):
        search_str = '%' + query + '%'
        cur = self.con.cursor()
        cur.execute('SELECT * FROM Book '
                    'WHERE ISBN LIKE %s OR Title LIKE %s OR Author LIKE %s',
                    (search_str, search_str, search_str))
        return cur.fetchall()
