"""
This module provides functions to run Master Pi Console Menu.
"""

import socket
from mp_app.book_function import BookFunction
from utils.menu_helper import MenuHelper


class MpConsole:
    """
    MpConsole class handles the Master Pi Console Menu function.

    Attributes:
        MSG (str): a default reply message.
        menu_items ([str]): a list of menu items to print.
        menu_end_number (int): the choice number for the last selectable item.
        __username (str, None): the username of the current logged in user.
        ___book_function (BookFunction, None): the BookFunction object
    """

    MSG = 'logout'

    def __init__(self):
        self.menu_items = [
            '*** Welcome to the Smart Library Management System! ***',
            'Search:',
            'Borrow:',
            'Return:',
            'Logout',
        ]
        self.menu_end_number = len(self.menu_items) - 1
        self.__username = None
        self.__book_function = None

    def start(self):
        """Receives username and starts the Master Pi program

        It will continue listening to port 65000 from all IP addresses and
        when message received, it will create a new BookFunction instance
        and run the main menu for the user.

        Once the user logs out, it will go back to listening for new messages.

        Returns:
            None

        """
        host = ''
        port = 65000
        address = (host, port)
        # Mp will always try to connect with client
        # this loop will not break
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            soc.bind(address)
            soc.listen()
            print("Listening on {}...".format(address))
            while True:
                print("Waiting for Reception Pi...")
                conn, addr = soc.accept()
                with conn:
                    print("Connected to {}".format(addr))
                    self.__username = conn.recv(4096)
                    if self.__username is not None:
                        self.__book_function = BookFunction(self.__username)
                        self.run_menu()
                        conn.sendall(MpConsole.MSG.encode('UTF-8'))
                        self.__username = None
                        self.__book_function = None

    def run_menu(self):
        """Runs the main menu

        It will keep showing the menu and asking for user selection until
        the user logs out.

        Returns:
            None

        """
        should_quit = False
        while not should_quit:
            MenuHelper.print_menu(self.menu_items)
            choice = MenuHelper.ask_for_input(self.menu_end_number)
            should_quit = self.__handle_choice(choice)

    def __handle_choice(self, choice):
        """Delegates user choice to corresponding class to handle

        Given the user choice, this method will create and call other
        class methods to handle the function.

        Args:
            choice: the user's choice of a menu item.

        Returns:
            bool: True if user chooses to logout, False otherwise.

        """
        if choice == 1:
            self.__book_function.search_for_book()
            return False
        if choice == 2:
            self.__book_function.borrow_book()
            return False
        if choice == 3:
            self.__book_function.return_book()
            return False
        print('Logging out...\n')
        return True
