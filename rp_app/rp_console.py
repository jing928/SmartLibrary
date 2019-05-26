"""
This module provides functions to run Reception Pi Console Menu.
"""

from rp_app.user_login import UserLogin
from rp_app.user_registration import UserRegistration
from utils.menu_helper import MenuHelper


class RpConsole:
    """
    RpConsole class handles the Reception Pi Console Menu function.

    Attributes:
        menu_items (list): a list of menu items to print.
        menu_end_number (int): the choice number for the last selectable item.
    """

    def __init__(self):
        self.menu_items = [
            '*** Welcome to the Smart Library Management System! ***',
            'Register:',
            'Login:',
            'Quit:'
        ]
        self.menu_end_number = len(self.menu_items) - 1

    def start(self):
        """Starts the console menu

        It will continue showing the menu and asking for selection
        unless the user chooses to quit.

        Returns:
            None

        """
        should_quit = False
        while not should_quit:
            MenuHelper.print_menu(self.menu_items)
            choice = MenuHelper.ask_for_input(self.menu_end_number)
            should_quit = RpConsole.__handle_choice(choice)

    @staticmethod
    def __handle_choice(choice):
        """Delegates user choice to corresponding class to handle

        Given the user choice, this method will create and call other
        class methods to handle the function.

        Args:
            choice: the user's choice of a menu item.

        Returns:
            bool: True if user chooses to quit, False otherwise.

        """
        if choice == 1:
            reg = UserRegistration()
            reg.start()
            return False
        if choice == 2:
            login = UserLogin()
            login.start()
            return False
        print('Quitting program...\n')
        return True
