import unittest
import pymysql as mysql
from mp_app.data_access_cloud import OrderedDictCursor, DataAccessCloud
from utils.file_access import FileAccess


class TestDataAccessCloud(unittest.TestCase):

    def setUp(self):
        db_config = FileAccess.json_to_dict('../db_config.json')
        self.connection = mysql.connect(host=db_config['HOST'],
                                        user=db_config['USER'],
                                        password=db_config['PASSWORD'],
                                        db='SmartLibraryTest',
                                        charset='utf8mb4',
                                        cursorclass=OrderedDictCursor)
        self.dao = DataAccessCloud(self.connection)
        cursor = self.connection.cursor()
        cursor.execute("""
                    create table LmsUser
                    (
                        LmsUserID int           not null auto_increment,
                        UserName  nvarchar(256) not null,
                        Name      text          not null,
                        constraint PK_LmsUser primary key (LmsUserID),
                        constraint UN_UserName unique (UserName)
                    );
        """)
        cursor.execute("""
                    create table Book
                    (
                        BookID        int                              not null auto_increment,
                        ISBN          nvarchar(20)                     not null,
                        Title         text                             not null,
                        Author        text                             not null,
                        PublishedDate date                             not null,
                        Status        enum ('available','unavailable') not null default 'available',
                        constraint PK_Book primary key (BookID),
                        constraint UN_ISBN unique (ISBN)
                    );
        """)
        cursor.execute("""
                    create table BookBorrowed
                    (
                        BookBorrowedID  int  not null auto_increment,
                        LmsUserID       int  not null,
                        BookID          int  not null,
                        Status          enum ('borrowed', 'returned'),
                        BorrowedDate    date not null,
                        ReturnedDate    date null,
                        CalendarEventID text,
                        constraint PK_BookBorrowed primary key (BookBorrowedID),
                        constraint FK_BookBorrowed_LmsUser foreign key (LmsUserID) references LmsUser (LmsUserID),
                        constraint FK_BookBorrowed_Book foreign key (BookID) references Book (BookID)
                    );
        """)
        cursor.execute("insert into Book (ISBN, Title, Author, PublishedDate) "
                       "values ('12345', 'Test Book', 'Tester', '2010-01-01');")
        cursor.execute("insert into LmsUser (UserName, Name) values ('test', 'test test');")
        self.connection.commit()

    def tearDown(self):
        cursor = self.connection.cursor()
        cursor.execute('drop table BookBorrowed;')
        cursor.execute('drop table LmsUser;')
        cursor.execute('drop table Book;')
        self.connection.commit()

    def test_search(self):
        result = self.dao.search('test')
        actual_book_name = result[0]['Title']
        expected_book_name = 'Test Book'
        self.assertTrue(actual_book_name == expected_book_name)

    def test_get_user_id(self):
        actual_user_id = self.dao.get_user_id('test')
        expected_user_id = 1
        self.assertTrue(actual_user_id == expected_user_id)

    def test_check_availability(self):
        expected = self.dao.check_availability(1)
        self.assertTrue(expected)

    def test_check_returnability(self):
        expected = self.dao.check_returnability(1)
        self.assertFalse(expected)


if __name__ == '__main__':
    unittest.main()
