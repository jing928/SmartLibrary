from rp_app.data_access_local import DataAccessLocal
from rp_app.encryptor import Encryptor
from rp_app.validator import Validator


class UserRegistration:

    def __init__(self):
        self.__dao = DataAccessLocal()
        self.__new_username = None
        self.__new_fullname = None
        self.__new_password = None

    def start(self):
        print('\n** New User Registration **\n')
        self.ask_for_username()
        self.ask_for_fullname()
        self.ask_for_password()
        self.register_user()

    def ask_for_username(self):
        is_valid = False
        while not is_valid:
            username = input('--> Enter the username here:\n'
                             '(Only letters and numbers are allowed, minimum 4 characters)')
            username = username.strip()
            is_input_valid = Validator.validate_username(username)
            username_exists = self.__dao.check_if_user_exists(username)
            is_valid = is_input_valid and not username_exists
            if not is_input_valid:
                print('Username entered does not meet the requirements...\n')
            if username_exists:
                print('The username already exists, please pick a new one.\n')

        self.__new_username = username

    def ask_for_fullname(self):
        is_valid = False
        while not is_valid:
            fullname = input('--> Enter your full name here\n'
                             '(Only <First Name> <Last Name> format is allowed. e.g. John Doe): ')
            fullname = fullname.strip()
            is_valid = Validator.validate_fullname(fullname)
            if not is_valid:
                print('Full name entered does not meet the requirements...\n')
        self.__new_fullname = fullname

    def ask_for_password(self):
        is_valid = False
        while not is_valid:
            password = input('--> Enter the password here\n'
                             '(At least one letter and one number, minimum 6 characters): ')
            password = password.strip()
            is_valid = Validator.validate_username(password)
            if not is_valid:
                print('Password entered does not meet the requirements...\n')
        password = Encryptor.encrypt(password)
        self.__new_password = password

    def register_user(self):
        if self.__new_username is None:
            print("Error: username wasn't saved correctly...")
            return
        if self.__new_fullname is None:
            print("Error: full name wasn't saved correctly...")
            return
        if self.__new_password is None:
            print("Error: password wasn't saved correctly...")
            return
        self.__dao.insert_user(username=self.__new_username,
                               fullname=self.__new_fullname,
                               password=self.__new_password)
        print('\nRegistration successful!\n')
