"""
This module provides functionality to handle login process.
"""

from utils.menu_helper import MenuHelper
from rp_app.login_with_password import LoginWithPassword
from rp_app.login_with_face import LoginWithFace


class UserLogin:

    def __init__(self):
        self.menu_items = [
            '*** Please choose login method ***',
            'Manual:',
            'Facial:',
            'Go back:'
        ]
        self.menu_end_number = len(self.menu_items) - 1

    def start(self):
        """
        Starts the user login process

        It will print menu include two login options, then user can make choice on login method.

        Returns:
            None
        """
        MenuHelper.print_menu(self.menu_items)
        choice = MenuHelper.ask_for_input(self.menu_end_number)
        UserLogin.__handle_choice(choice)


@staticmethod
def __handle_choice(choice):
    if choice == 1:
        login_with_password = LoginWithPassword()
        login_with_password.start()
    elif choice == 2:
        login_with_face = LoginWithFace()
        login_with_face.login()
