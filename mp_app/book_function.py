"""
This module provides functionality for search, borrow, and return a book.
"""

from datetime import date, timedelta
from tabulate import tabulate
from mp_app.data_access_cloud import DataAccessCloud
from utils.calendar_access import CalendarAccess
from utils.qr_code_scanner import QrCodeScanner
from utils.voice_to_text import VoiceToText


class BookFunction:
    """
    BookFunction class handles search, borrow, and return a book for a specific user.

    Attributes:
        __username (str): the username of the current user.
        __dao (DataAccessCloud): a data access object to communicate with the cloud database.
        __cal (CalendarAccess): a calendar access object to communicate with Google Calendar.
        __user_id (str): the internal ID of the current user.
        __search_result (str, None): saves the last search result made by the user.
    """

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
        """Helps user search for a book to borrow

        It first asks user for the search query and then calls the data
        access object to handle the search.

        If nothing matches the query, returns, otherwise, format, save,
        and print the results to stdout.

        Returns:
            None

        """
        query = input('You can search by title, ISBN, or author.\n'
                      '--> Please enter your search keywords here: ')
        self.__search_helper(query)

    def search_for_book_voice(self):
        """Helps user search for a book using voice

        It calls the VoiceToText class to handle recording and transcribing
        the voice and then uses the query to search and prints out the
        results to stdout.

        Returns:
            None

        """
        print('Starting microphone service...\n')
        voice_to_text = VoiceToText()
        query = voice_to_text.transcribe()
        if query is None:
            return
        self.__search_helper(query)

    def __search_helper(self, query):
        result = self.__dao.search(query)
        if not result:
            print('Sorry...there is no book matching the keywords.\n')
            return
        self.__search_result = BookFunction.__format_table(result)
        print(self.__search_result)

    def borrow_book(self):
        """Helps user borrow a book

        If the user hasn't searched, it will ask the user to search first and return.
        If the user has searched, it will print the previous search results and asks
        user to make a selection of one or more books to borrow.

        Then it will call __borrow_helper to process borrow for each of the selected books.

        Returns:
            None

        """
        if self.__search_result is None:
            print('Please search for a book first...')
            return
        print('** Below is your previous search result **\n')
        print(self.__search_result)
        book_ids = BookFunction.__ask_for_book_ids(self.__dao.check_availability)
        for book_id in book_ids:
            self.__borrow_helper(book_id)

    def return_book(self):
        """Helps user return a book

        If the user has unreturned books, it will print out the list of borrowed books,
        otherwise return.

        Then it will ask the user to select one or more books to return and call __return_helper
        method to process each of the selected books.

        Returns:
            None

        """
        books_borrowed = self.__dao.list_borrowed_books(self.__user_id)
        if not books_borrowed:
            print("You haven't borrowed any book. Nothing to return.")
            return
        BookFunction.__print_borrowed_books(books_borrowed)
        book_ids = BookFunction.__ask_for_book_ids(self.__dao.check_returnability)
        for book_id in book_ids:
            self.__return_helper(book_id)

    def return_book_with_qr_code(self):
        """Helps user return a book by scanning a QR code of the book

        If the user has unreturned books, it will print out the list of borrowed books,
        otherwise return.

        Then it will ask the user to scan the QR code of the book to return.

        Returns:
            None

        """
        books_borrowed = self.__dao.list_borrowed_books(self.__user_id)
        if not books_borrowed:
            print("You haven't borrowed any book. Nothing to return.")
            return
        BookFunction.__print_borrowed_books(books_borrowed)
        book_ids = QrCodeScanner().scan()
        for book_id in book_ids:
            if self.__dao.check_returnability(book_id):
                self.__return_helper(book_id)

    @staticmethod
    def __print_borrowed_books(books_borrowed):
        print('** Below are the book(s) you have borrowed: **\n')
        print(BookFunction.__format_table(books_borrowed))

    def __borrow_helper(self, book_id):
        """Facilitates borrowing a specific book

        It creates a calendar event on the due date (one week after today),
        and then creates a new book borrowing transaction in the database.

        Args:
            book_id: the ID of the book to be borrowed.

        Returns:
            None

        """
        borrow_date = date.today()
        due_date = borrow_date + timedelta(days=7)
        detail = self.__create_event_detail(book_id)
        event_id = self.__cal.add_due_date_event(detail['summary'], detail['description'],
                                                 due_date)
        self.__dao.borrow_book(book_id, self.__user_id, borrow_date, event_id)
        print('Book successfully borrowed!')

    def __return_helper(self, book_id):
        """Facilitates returning a specific book

        It deletes the calendar event for this book on the due date, and
        then update the book borrowing transaction and book status.

        Args:
            book_id: the ID of the book to be returned.

        Returns:
            None

        """
        return_date = date.today()
        book_borrowed_id = self.__dao.get_book_borrowed_id(book_id, self.__user_id)
        event_id = self.__dao.get_calendar_event_id(book_borrowed_id)
        self.__cal.delete_event(event_id)
        self.__dao.return_book(book_id, self.__user_id, return_date)
        print('Book successfully returned!')

    def __create_event_detail(self, book_id):
        """Creates detailed info for a specific book to be borrowed

        It first retrieves the book details from the database and then
        formats it to be used in creating calendar event.

        Args:
            book_id: the ID of the book to get information.

        Returns:
            dict: a dictionary of summary and description of the event.

        """
        details = self.__dao.get_book_details(book_id)
        book_title = details['Title']
        summary = 'Return {title}'.format(title=book_title)
        desc = 'Book Borrowed: {title} by {author}\n' \
               'Borrower: {username}'.format(title=book_title, author=details['Author'],
                                             username=self.__username)
        return {'summary': summary, 'description': desc}

    @staticmethod
    def __ask_for_book_id(check_eligibility):
        """Prompts user to select a book ID

        It will continue asking user to enter the book id unless
        the user chooses to quit by entering 'q' or an eligible book
        is found.

        Args:
            check_eligibility: a function to check if the book is eligible
            for the selected operation.

        Returns:
            str: q if the user chooses to quit.
            int: the ID of the book found.

        """
        book_found = False
        while not book_found:
            input_id = input('--> Please enter the BookID here: ')
            if input_id == 'q':
                book_id = input_id
                break
            if input_id.isdigit():
                book_id = int(input_id)
                book_found = check_eligibility(book_id)
            else:
                print('Error: please only enter a positive integer number.')
        return book_id

    @staticmethod
    def __ask_for_book_ids(check_eligibility):
        """Prompts user to enter multiple book IDs

        It will keeping calling __ask_for_book_id until it receives 'q'. For each
        integer id it receives, it will append it to a list.

        Args:
            check_eligibility: a function to check if the book is eligible
            for the selected operation.

        Returns:
            list: a list of book IDs.

        """
        ended = False
        book_ids = []
        while not ended:
            print('\nContinue entering BookID or enter "q" to stop.')
            book_id = BookFunction.__ask_for_book_id(check_eligibility)
            if book_id == 'q':
                ended = True
            else:
                book_ids.append(book_id)
        return book_ids

    @staticmethod
    def __format_table(rows):
        """Nicely format a table retrieved from the database using Tabulate

        Args:
            rows (dict): a dictionary representation of a table.

        Returns:
            str: a nicely formatted string of the table content.

        """
        return tabulate(rows, headers='keys', tablefmt='simple')
