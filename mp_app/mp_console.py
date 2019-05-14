#!/usr/bin/env python3
# Reference: https://realpython.com/python-sockets/
# Documentation: https://docs.python.org/3/library/socket.html
import socket
from utils.menu_helper import MenuHelper


class MpConsole:
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

    def start(self):
        """receive username and start Mp program"""
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
                    if self.__username:
                        self.run_menu()
                        conn.sendall(MpConsole.MSG.encode('UTF-8'))
                        self.__username = None

    def run_menu(self):
        should_quit = False
        while not should_quit:
            MenuHelper.print_menu(self.menu_items)
            choice = MenuHelper.ask_for_input(self.menu_end_number)
            should_quit = MpConsole.__handle_choice(choice)

    @staticmethod
    def __handle_choice(choice):
        if choice == 1:
            print('search')
            return False
        if choice == 2:
            print('borrow')
            return False
        if choice == 3:
            print('return')
            return False
        print('Logging out...\n')
        return True
