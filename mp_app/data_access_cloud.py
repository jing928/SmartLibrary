from datetime import date

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
        cur = self.con.cursor()
        search_str = '%' + query + '%'
        cur.execute('SELECT * FROM Book '
                    'WHERE ISBN LIKE %s OR Title LIKE %s OR Author LIKE %s',
                    (search_str, search_str, search_str))
        return cur.fetchall()

    def get_user_id(self, username):
        cur = self.con.cursor()
        cur.execute('SELECT LmsUserID FROM LmsUser WHERE UserName = %s', username)
        result = cur.fetchone()
        if result is None:
            print("User doesn't exist.")
            return result
        return result['LmsUserID']

    def check_availability(self, book_id):
        cur = self.con.cursor()
        cur.execute('SELECT Status FROM Book WHERE BookID = %s', book_id)
        result = cur.fetchone()
        if result is None:
            print("The book doesn't exist.")
            return False
        status = result['Status']
        if status == 'available':
            return True
        if status == 'unavailable':
            print('The book is not available.')
            return False
        print('Something went wrong...')
        return False

    def borrow_book(self, book_id, user_id):
        cur = self.con.cursor()
        borrow_date = date.today()
        cur.execute('INSERT INTO BookBorrowed (LmsUserID, BookID, Status, BorrowedDate)'
                    'VALUES (%s, %s, %s, %s)', (user_id, book_id, 'borrowed', borrow_date))
        cur.execute('UPDATE Book SET Status = %s WHERE BookID = %s', ('unavailable', book_id))
        self.con.commit()

    def return_book(self, book_id, user_id):
        cur = self.con.cursor()
        return_date = date.today()
        book_borrowed_id = self.__get_book_borrowed_id(book_id, user_id)
        cur.execute('UPDATE BookBorrowed SET Status = %s, ReturnedDate = %s '
                    'WHERE BookBorrowedID = %s', ('returned', return_date, book_borrowed_id))
        cur.execute('UPDATE Book SET Status = %s WHERE BookID = %s', ('available', book_id))
        self.con.commit()

    def __get_book_borrowed_id(self, book_id, user_id):
        cur = self.con.cursor()
        cur.execute('SELECT BookBorrowedID FROM BookBorrowed '
                    'WHERE BookID = %s AND LmsUserID = %s AND ReturnedDate IS NULL',
                    (book_id, user_id))
        return cur.fetchone()['BookBorrowedID']

    def list_borrowed_books(self, user_id):
        cur = self.con.cursor()
        cur.execute('SELECT BookID, Status, BorrowedDate FROM BookBorrowed '
                    'WHERE LmsUserID = %s AND ReturnedDate IS NULL ', user_id)
        return cur.fetchall()