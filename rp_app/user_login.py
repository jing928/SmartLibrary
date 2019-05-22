"""
This module provides functionality to handle login process.
"""

import socket
from utils.file_access import FileAccess
from utils.encryptor import Encryptor
from rp_app.data_access_local import DataAccessLocal


class UserLogin:
    """
    UserLogin class handles user login process.

    Attributes:
        __dao (DataAccessLocal): data access object to the local database.
        __server_ip (str): the IP address of the Master Pi.
        __username (str, None): the username of the logging user.
        __password (str, None): the password of the logging user.
    """

    def __init__(self):
        self.__dao = DataAccessLocal()
        ip_dict = FileAccess.get_ip_config()
        self.__server_ip = ip_dict["ip"]
        self.__username = None
        self.__password = None

    def start(self):
        """Starts the user login process

        It calls a series of other methods to complete the process.

        Returns:
            None

        """
        print('\n** User Login **\n')
        self.ask_for_username()
        self.ask_for_password()
        self.login_user()

    def ask_for_username(self):
        """Prompts user to enter the username

        Returns:
            None

        """
        username = input('--> Enter the username here: ')
        username = username.strip()
        self.__username = username

    def ask_for_password(self):
        """Prompts user to enter the password

        Returns:
            None

        """
        password = input('--> Enter the password here: ')
        password = password.strip()
        self.__password = password

    def login_user(self):
        """Logs user in

        It checks if the username exists, if not then return.
        It then checks if the password is correct, if not then return.
        If everything is correct, it sends user info to the Master Pi.

        Returns:
            None

        """
        username_exists = self.__dao.check_if_user_exists(self.__username)
        if not username_exists:
            print("Username doesn't exist...")
            return

        hashed_password = self.__dao.get_password_for_user(self.__username)
        password_correct = Encryptor.verify(self.__password, hashed_password)
        if not password_correct:
            print('Incorrect password.\n')
            return
        UserLogin.send_message(self.__username, self.__server_ip)

    @staticmethod
    def send_message(msg, server_ip):
        """Sends message to server using sockets

        It sends the message to the server and then waits for
        reply. While waiting, it will pause the program and show
        'Busy'.

        Args:
            msg: the message to be sent
            server_ip: the IP address of the server

        Returns:
            None

        """
        # Reference: https://realpython.com/python-sockets/
        # Documentation: https://docs.python.org/3/library/socket.html

        host = server_ip
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
