"""
This module provides functions to help with console UI menus.
"""


class MenuHelper:
    """
    MenuHelper class provides common methods to help with building menus.
    """

    @staticmethod
    def print_menu(menu_items):
        """Creates a menu with given items.

        Args:
            menu_items: a list items to be used as menu items.

        Returns:
            None: no return value as it prints menu to the stdout.

        """
        for index, item in enumerate(menu_items):
            if index == 0:
                print(item)
                print('\n')
            else:
                menu_item = "{item:<9s} {choice:>1d}".format(item=item,
                                                             choice=index)
                print(menu_item)

    @staticmethod
    def ask_for_input(menu_end_number):
        """Asks user for menu choices.

        It asks, validates and returns the user entered choices.

        Args:
            menu_end_number: The choice number that corresponds to the last menu item.

        Returns:
            int: the choice the user enters.

        """
        menu_start_number = 1
        choice = 0
        while choice > menu_end_number or choice < menu_start_number:
            input_string = input('\n--> Enter your choice here: ')
            if input_string.isdigit():
                choice = int(input_string)
            else:
                choice = 0
            if choice > menu_end_number or choice < menu_start_number:
                print('Invalid input: the choice must be an integer that '
                      'corresponds to the menu item.')
        return choice
