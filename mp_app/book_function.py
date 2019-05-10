from datetime import date, timedelta

from tabulate import tabulate
from mp_app.data_access_cloud import DataAccessCloud
from utils.calendar_access import CalendarAccess


class BookFunction:

    def __init__(self, username):
        self.__username = username
        self.__dao = DataAccessCloud()
        self.__cal = CalendarAccess()
        user_id = self.__dao.get_user_id(username)
        if user_id is None:
            raise Exception('Username does not exist.')
        self.__user_id = user_id
        self.__search_result = None

    def search_for_book(self):
        query = input('You can search by title, ISBN, or author.\n'
                      '--> Please enter your search keywords here: ')
        result = self.__dao.search(query)
        if not result:
            print('Sorry...there is no book matching the keywords.\n')
            return
        self.__search_result = BookFunction.__format_table(result)
        print(self.__search_result)

    def borrow_book(self):
        if self.__search_result is None:
            print('Please search for a book first...')
            return
        print('** Below is your previous search result **\n')
        print(self.__search_result)
        book_id = BookFunction.__ask_for_book_id(self.__dao.check_availability)
        self.__borrow_helper(book_id)

    def return_book(self):
        books_borrowed = self.__dao.list_borrowed_books(self.__user_id)
        if not books_borrowed:
            print("You haven't borrowed any book. Nothing to return.")
            return
        print('** Below are the book(s) you have borrowed: **\n')
        print(BookFunction.__format_table(books_borrowed))
        book_id = BookFunction.__ask_for_book_id(self.__dao.check_returnability)
        self.__return_helper(book_id)

    def __borrow_helper(self, book_id):
        borrow_date = date.today()
        due_date = borrow_date + timedelta(days=7)
        detail = self.__create_event_detail(book_id)
        event_id = self.__cal.add_due_date_event(detail['summary'], detail['description'],
                                                 due_date)
        self.__dao.borrow_book(book_id, self.__user_id, borrow_date, event_id)
        print('Book successfully borrowed!')

    def __return_helper(self, book_id):
        return_date = date.today()
        book_borrowed_id = self.__dao.get_book_borrowed_id(book_id, self.__user_id)
        event_id = self.__dao.get_calendar_event_id(book_borrowed_id)
        self.__cal.delete_event(event_id)
        self.__dao.return_book(book_id, self.__user_id, return_date)
        print('Book successfully returned!')

    def __create_event_detail(self, book_id):
        details = self.__dao.get_book_details(book_id)
        book_title = details['Title']
        summary = 'Return {title}'.format(title=book_title)
        desc = 'Book Borrowed: {title} by {author}\n' \
               'Borrower: {username}'.format(title=book_title, author=details['Author'],
                                             username=self.__username)
        return {'summary': summary, 'description': desc}

    @staticmethod
    def __ask_for_book_id(check_eligibility):
        book_found = False
        while not book_found:
            input_id = input('\n--> Please enter the BookID here: ')
            if input_id.isdigit():
                book_id = int(input_id)
                book_found = check_eligibility(book_id)
            else:
                print('Error: please only enter a positive integer number.')
        return book_id

    @staticmethod
    def __format_table(rows):
        return tabulate(rows, headers='keys', tablefmt='simple')
