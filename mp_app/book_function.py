from tabulate import tabulate
from mp_app.data_access_cloud import DataAccessCloud


class BookFunction:

    def __init__(self, username):
        self.__username = username
        self.__dao = DataAccessCloud()
        user_id = self.__dao.get_user_id(username)
        if user_id is None:
            raise Exception('Username does not exist.')
        self.__user_id = user_id
        self.__search_result = None

    def search(self):
        query = input('You can search by title, ISBN, or author.\n'
                      '--> Please enter your search keywords here: ')
        result = self.__dao.search(query)
        if not result:
            print('Sorry...there is no book matching the keywords.\n')
            return
        self.__search_result = tabulate(result, headers='keys', tablefmt='simple')
        print(self.__search_result)

    def borrow(self):
        if self.__search_result is None:
            print('Please search for a book first...')
            return
        print('** Below is your previous search result **\n')
        print(self.__search_result)
        book_id = self.__ask_for_book_id()
        self.__dao.borrow_book(book_id, self.__user_id)
        # TODO: add event to Google Calendar
        print('Book successfully borrowed!')

    def __ask_for_book_id(self):
        book_found = False
        while not book_found:
            input_id = input('--> Please enter the BookID here: ')
            if input_id.isdigit():
                book_id = int(input_id)
                book_found = self.__dao.check_availability(book_id)
            else:
                print('Error: please only enter a positive integer number.')
        return book_id
