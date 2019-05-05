import socket
from rp_app.encryptor import Encryptor
from rp_app.data_access_local import DataAccess


class UserLogin:

    def __init__(self):
        self.__dao = DataAccess()
        self.__username = None
        self.__password = None

    def start(self):
        print('\n** User Login **\n')
        self.ask_for_username()
        self.ask_for_password()
        self.login_user()

    def ask_for_username(self):
        username = input('--> Enter the username here:\n'
                         '(Only letters and numbers are allowed, minimum 4 characters)')
        username = username.strip()
        self.__username = username

    def ask_for_password(self):
        password = input('--> Enter the password here:\n'
                         '(At least one letter and one number, minimum 6 characters)')
        password = password.strip()
        self.__password = password

    def login_user(self):
        username_exists = self.__dao.check_if_user_exists(self.__username)

        if username_exists:
            is_valid = False
            while not is_valid:
                hashed_password = self.__dao.get_password_for_user(self.__username)
                password_correct = Encryptor.verify(self.__password, hashed_password)

                is_valid = password_correct

                if not password_correct:
                    print('Password or Username error(1)\n')  # misleading info
                    self.start()
                    return False

            UserLogin.send_message(self.__username)
            return True
        print('Password or Username error(2)\n')
        self.start()
        return False

    @staticmethod
    def send_message(msg):
        """ use TCP connection"""
        # !/usr/bin/env python3
        # Reference: https://realpython.com/python-sockets/
        # Documentation: https://docs.python.org/3/library/socket.html
        # HOST = input("Enter IP address of server: ")

        host = "10.132.54.199"  # The server's hostname or IP address.
        port = 65000  # The port used by the server.
        address = (host, port)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            print("Connecting to {}...".format(address))
            soc.connect(address)
            print('connected')
            print("Busy")

            message = msg
            soc.sendall(message.encode())

            while True:
                data = soc.recv(4096)
                if data.decode('UTF-8') == "logout":
                    print("Received {} bytes of data decoded to: '{}'".format(
                        len(data), data.decode()))
                    break
            print("Disconnecting from server.")
        print("Done.")
