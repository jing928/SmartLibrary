#!/usr/bin/env python3
# Reference: https://realpython.com/python-sockets/
# Documentation: https://docs.python.org/3/library/socket.html
import socket


class MpConsole:
    menu_items = [
            '*** Welcome to the Smart Library Management System! ***',
            'Search:',
            'Borrow:',
            'Return:',
            'Logout',
        ]
    menu_end_number = len(menu_items) - 1

    def __init__(self):
        """ initialize vairables """

        self.__username = None
        self.msg = 'logout'       
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = ""
        self.port = 65000
        self.address = (self.host, self.port)
        

    def start(self):
        """receive username and start Mp program"""
        while True:
        # Mp will always try to connect with client
        # this loop will not break
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(self.address)
                s.listen()
                print('is listening')                        
                print("Listening on {}...".format(self.address))
                while True:
                    print("Waiting for Reception Pi...")
                    conn, addr = s.accept()
                    with conn:
                        while True:                                                       
                            self.__username =conn.recv(4096)                           
                            if self.__username:
                                MpConsole.print_menu(self.menu_items)
                                choice = MpConsole.ask_for_input(self.menu_end_number)
                                MpConsole.handle_choice(choice)
                                conn.sendall(self.msg.encode('UTF-8'))
                                self.__username = None
                                break            
                    continue #keep listening
                    

    @staticmethod
    def handle_choice(choice):
        flag = True
        while flag is True:
            if choice == 1:
                print('search') 
                MpConsole.print_menu(MpConsole.menu_items)
                choice = MpConsole.ask_for_input(MpConsole.menu_end_number)         
            elif choice == 2:
                print('borrow')
                MpConsole.print_menu(MpConsole.menu_items)
                choice = MpConsole.ask_for_input(MpConsole.menu_end_number)    
            elif choice == 3:
                print('return')
                MpConsole.print_menu(MpConsole.menu_items)
                choice = MpConsole.ask_for_input(MpConsole.menu_end_number)    
            elif choice == 4:
                print('logout')
                flag = False
                

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
            input_string = input('\n--> Enter your choice here:')
            if input_string.isdigit():
                choice = int(input_string)
            else:
                choice = 0
            if choice > menu_end_number or choice < menu_start_number:
                print('Invalid input: the choice must be an integer that '
                      'corresponds to the menu item.')
        return choice
