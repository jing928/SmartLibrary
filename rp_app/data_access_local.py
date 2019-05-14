import sqlite3 as lite


class DataAccessLocal:

    def __init__(self, connection=None):
        if connection is None:
            connection = lite.connect('rp_local.db',
                                      detect_types=lite.PARSE_DECLTYPES | lite.PARSE_COLNAMES)
        self.con = connection
        with self.con:
            cur = self.con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS LMUSER "
                        "(username TEXT PRIMARY KEY, "
                        "fullname TEXT NOT NULL, password TEXT NOT NULL)")

    def close(self):
        self.con.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

    def insert_user(self, username, fullname, password):
        cur = self.con.cursor()
        cur.execute("INSERT INTO LMUSER (username, fullname, password) "
                    "VALUES (?, ?, ?)", (username, fullname, password))
        self.con.commit()

    def check_if_user_exists(self, username):
        cur = self.con.cursor()
        cur.execute("SELECT EXISTS (SELECT 1 FROM LMUSER WHERE username = ?)", (username,))
        result = cur.fetchone()[0]
        if result == 0:
            return False
        return True

    def get_password_for_user(self, username):
        cur = self.con.cursor()
        cur.execute("SELECT password FROM LMUSER WHERE username = ?", (username,))
        result = cur.fetchone()[0]
        return result
