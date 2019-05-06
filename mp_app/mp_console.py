#!/usr/bin/env python3
# Reference: https://realpython.com/python-sockets/
# Documentation: https://docs.python.org/3/library/socket.html
import socket


class MpConsole:


    def __init__(self):
        """ initialize connection """
        # not sure if we can initialize connection in construction

        self.menu_items = [
            '*** Welcome to the Smart Library Management System! ***',
            'Search:',
            'Borrow:',
            'Return:',
            'Logout',
        ]
        self.menu_end_number = len(self.menu_items) - 1
        self.__username = None
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = ""              # Empty string means to listen on all IP's on the machine, also works with IPv6.
                                    # Note "0.0.0.0" also works but only with IPv4.
        self.PORT = 65000           # Port to listen on (non-privileged ports are > 1023).
        self.ADDRESS = (self.HOST, self.PORT)
        self.sock.bind(self.ADDRESS)
        self.sock.listen()      #from here Mp starts listening
        self.logout_msg = "logout"      #this is a final variable
        



    def start(self):   
        
        """recieve username and start Mp program"""

        # Mp will always try to connect with client
        # this loop will not break
        while True:
            print('waiting for a connection')

            #connect with client (Rp)   
            connection,client_address = self.sock.accept()         
            try:
                print('connection from', client_address)
                
                while True:

                    #trying to get username from Rp, if succefully get username, start program on Mp
                    self.username = connection.recv(4096)

                    if self.username:

                        MpConsole.print_menu(self.menu_items)
                        choice = MpConsole.ask_for_input(self.menu_end_number)

                        if choice is not 4:                                                                                     
                            self.__handle_choice(choice)

                        # choice == 4 means log out, program will break connection loop to diconnected from client
                        # then send logout message 
                        else:
                            self.sock.sendall(self.logout_msg.encode())                                                                                                           
                            break
            
            finally:
                # Clean up the connection
                connection.close()
                print('disconnect from client')
            

        

    def __handle_choice(self, choice):

        if choice == 1:            
            print('search')

        elif choice == 2:
            
            print('borrow')
        elif choice == 3:
            
            print('return')

        

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



 



