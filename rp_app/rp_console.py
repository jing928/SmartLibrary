from rp_app.user_login import UserLogin
from rp_app.user_registration import UserRegistration


class RpConsole:

    def __init__(self):
        self.menu_items = [
            '*** Welcome to the Smart Library Management System! ***',
            'Register:',
            'Login:',
            'Quit'
        ]
        self.menu_end_number = len(self.menu_items) - 1

    def start(self):
        should_quit = False
        while not should_quit:
            RpConsole.print_menu(self.menu_items)
            choice = RpConsole.ask_for_input(self.menu_end_number)
            should_quit = self.__handle_choice(choice)

    @staticmethod
    def __handle_choice(choice):
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

    @staticmethod
    def print_menu(menu_items):
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
