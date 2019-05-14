import socket
from utils.file_access import FileAccess
from rp_app.encryptor import Encryptor
from rp_app.data_access_local import DataAccessLocal


class UserLogin:

    def __init__(self):
        self.__dao = DataAccessLocal()
        ip_dict = FileAccess.get_ip_config()
        self.__server_ip = ip_dict["ip"]
        self.__username = None
        self.__password = None

    def start(self):
        print('\n** User Login **\n')
        self.ask_for_username()
        self.ask_for_password()
        self.login_user()

    def ask_for_username(self):
        username = input('--> Enter the username here:')
        username = username.strip()
        self.__username = username

    def ask_for_password(self):
        password = input('--> Enter the password here:')
        password = password.strip()
        self.__password = password

    def login_user(self):
        username_exists = self.__dao.check_if_user_exists(self.__username)
        if not username_exists:
            print("Username doesn't exist...")
            return False

        hashed_password = self.__dao.get_password_for_user(self.__username)
        password_correct = Encryptor.verify(self.__password, hashed_password)
        if not password_correct:
            print('Incorrect password.\n')
            return False
        UserLogin.send_message(self.__username, self.__server_ip)
        return True

    @staticmethod
    def send_message(msg, server_ip):
        """ use TCP connection"""
        # !/usr/bin/env python3
        # Reference: https://realpython.com/python-sockets/
        # Documentation: https://docs.python.org/3/library/socket.html
        # HOST = input("Enter IP address of server: ")

        host = server_ip  # The server's hostname or IP address.
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
