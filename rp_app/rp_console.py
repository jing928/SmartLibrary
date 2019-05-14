from rp_app.user_login import UserLogin
from rp_app.user_registration import UserRegistration
from utils.menu_helper import MenuHelper


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
            MenuHelper.print_menu(self.menu_items)
            choice = MenuHelper.ask_for_input(self.menu_end_number)
            should_quit = RpConsole.__handle_choice(choice)

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
