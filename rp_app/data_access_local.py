import sqlite3 as lite


class DataAccess:

    def __init__(self, in_memory=False):
        if in_memory:
            self.con = lite.connect(':memory:',
                                    detect_types=lite.PARSE_DECLTYPES | lite.PARSE_COLNAMES)
        else:
            self.con = lite.connect('rp_local.db',
                                    detect_types=lite.PARSE_DECLTYPES | lite.PARSE_COLNAMES)
        with self.con:
            cur = self.con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS LMUSER "
                        "(username TEXT PRIMARY KEY, "
                        "fullname TEXT NOT NULL, password TEXT NOT NULL)")

    def __del__(self):
        self.con.close()

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
