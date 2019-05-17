"""
This module provides functions to interact with cloud database.
"""

from collections import OrderedDict
import pymysql as mysql
from utils.file_access import FileAccess


class DataAccessCloud:
    """
    DataAccessCloud class provides methods to handle common SQL operations.
    """

    def __init__(self, connection=None):
        """Constructor

        It creates a new MYSQL connection with configurations from db_config.json
        if no connection is passed in.

        Args:
            connection: a MySQL connection
        """
        if connection is None:
            db_config = FileAccess.get_db_config()
            connection = mysql.connect(host=db_config['HOST'],
                                       user=db_config['USER'],
                                       password=db_config['PASSWORD'],
                                       db=db_config['DATABASE'],
                                       charset='utf8mb4',
                                       cursorclass=OrderedDictCursor)
        self.con = connection

    def close(self):
        """Closes the connection

        Returns:
            None

        """
        self.con.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

    def search(self, query):
        """Search for a book with a given query

        It will search all three columns - ISBN, title, and Author.
        Any match will count as found.

        Args:
            query: a string of search text

        Returns:
            list: a table of found books.

        """
        cur = self.con.cursor()
        search_str = '%' + query + '%'
        cur.execute('SELECT * FROM Book '
                    'WHERE ISBN LIKE %s OR Title LIKE %s OR Author LIKE %s',
                    (search_str, search_str, search_str))
        return cur.fetchall()

    def get_user_id(self, username):
        """Get user ID with a given username

        It finds and returns the primary key of a username

        Args:
            username: the username whose ID is wanted.

        Returns:
            str: the user ID

        """
        cur = self.con.cursor()
        cur.execute('SELECT LmsUserID FROM LmsUser WHERE UserName = %s', username)
        result = cur.fetchone()
        if result is None:
            print("User doesn't exist.")
            return result
        return result['LmsUserID']

    def check_availability(self, book_id):
        """Check if a book is available

        Args:
            book_id: the ID of the book to be checked.

        Returns:
            bool: True if the status is available, False otherwise.

        """
        result = self.__get_book_status(book_id)
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

    def check_returnability(self, book_id):
        """Check if a book can be returned

        Args:
            book_id: the ID of the book to be checked.

        Returns:
            bool: True if the status is unavailable, False otherwise.

        """
        result = self.__get_book_status(book_id)
        if result is None:
            print("The book doesn't exist.")
            return False
        status = result['Status']
        if status == 'unavailable':
            return True
        if status == 'available':
            print('The book is not borrowed.')
            return False
        print('Something went wrong...')
        return False

    def __get_book_status(self, book_id):
        cur = self.con.cursor()
        cur.execute('SELECT Status FROM Book WHERE BookID = %s', book_id)
        result = cur.fetchone()
        return result

    def borrow_book(self, book_id, user_id, borrow_date, event_id):
        """Borrow a book

        It sets the book status to unavailable and creates a new book borrowed
        record.

        Args:
            book_id: the ID of the book to be borrowed.
            user_id: the ID of the borrower.
            borrow_date: the date of the borrow.
            event_id: the ID of the calendar event on the due date.

        Returns:
            None

        """
        cur = self.con.cursor()
        cur.execute('INSERT INTO BookBorrowed '
                    '(LmsUserID, BookID, Status, BorrowedDate, CalendarEventID)'
                    'VALUES (%s, %s, %s, %s, %s)',
                    (user_id, book_id, 'borrowed', borrow_date, event_id))
        cur.execute('UPDATE Book SET Status = %s WHERE BookID = %s', ('unavailable', book_id))
        self.con.commit()

    def return_book(self, book_id, user_id, return_date):
        """Return a book

        It sets the book status to available and updates the corresponding
        book borrowed record to have a status of returned and null event id.

        Args:
            book_id: the ID of the book to be returned.
            user_id: the ID of the borrower.
            return_date: the date of the return.

        Returns:
            None

        """
        cur = self.con.cursor()
        book_borrowed_id = self.get_book_borrowed_id(book_id, user_id)
        cur.execute('UPDATE BookBorrowed '
                    'SET Status = %s, ReturnedDate = %s, CalendarEventID = NULL '
                    'WHERE BookBorrowedID = %s', ('returned', return_date, book_borrowed_id))
        cur.execute('UPDATE Book SET Status = %s WHERE BookID = %s', ('available', book_id))
        self.con.commit()

    def get_book_borrowed_id(self, book_id, user_id):
        """Find the ID of the book borrowed record

        Args:
            book_id: the ID of the book borrowed.
            user_id: the ID of the borrower.

        Returns:
            str: the ID of the book borrowed record.

        """
        cur = self.con.cursor()
        cur.execute('SELECT BookBorrowedID FROM BookBorrowed '
                    'WHERE BookID = %s AND LmsUserID = %s AND ReturnedDate IS NULL',
                    (book_id, user_id))
        return cur.fetchone()['BookBorrowedID']

    def get_calendar_event_id(self, book_borrowed_id):
        """Retrieve the calendar event ID

        Args:
            book_borrowed_id: the ID of the book borrowed record.

        Returns:
            str: calendar event ID

        """
        cur = self.con.cursor()
        cur.execute('SELECT CalendarEventID FROM BookBorrowed '
                    'WHERE BookBorrowedID = %s', book_borrowed_id)
        return cur.fetchone()['CalendarEventID']

    def list_borrowed_books(self, user_id):
        """List all borrowed books of a user.

        Args:
            user_id: the ID of the borrower.

        Returns:
            list: a table of books borrowed.

        """
        cur = self.con.cursor()
        cur.execute('SELECT BookID, Status, BorrowedDate FROM BookBorrowed '
                    'WHERE LmsUserID = %s AND ReturnedDate IS NULL ', user_id)
        return cur.fetchall()

    def get_book_details(self, book_id):
        """Get details of a book

        Args:
            book_id: the ID of the book.

        Returns:
            dict: a dictionary of the book details

        """
        cur = self.con.cursor()
        cur.execute('SELECT * FROM Book WHERE BookID = %s', book_id)
        return cur.fetchone()


class OrderedDictCursor(mysql.cursors.DictCursorMixin, mysql.cursors.Cursor):
    """
    OrderedDicCursor class uses mysql.cursors.DictCursorMixin to implement a
    new type of cursor to allow returned dictionary has the same column order
    as the database schema.
    """
    dict_type = OrderedDict
