from rp_app.validator import Validator
from rp_app.encryptor import Encryptor
from rp_app.data_access_local import DataAccess
import socket

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
        is_valid = False
        while not is_valid:
            username = input('--> Enter the username here:\n'
                             '(Only letters and numbers are allowed, minimum 4 characters)')
            username = username.strip()
            is_input_valid = Validator.validate_username(username)           
            is_valid = is_input_valid
            if not is_input_valid:
                print('Username entered does not meet the requirements...\n')
            

        self.__username = username

    def ask_for_password(self):
        is_valid = False
        while not is_valid:
            password = input('--> Enter the password here:\n'
                             '(At least one letter and one number, minimum 6 characters)')
            password = password.strip()
            is_valid = Validator.validate_username(password)
            if not is_valid:
                print('Password entered does not meet the requirements...\n')
        
        self.__password = password

    def login_user(self):
   
        username_exists = self.__dao.check_if_user_exists(self.__username)

        if username_exists:
            is_valid = False
            while not is_valid:
                hashed_password = self.__dao.get_password_for_user(self.__username)
                password_correct = Encryptor.verify(self.__password,hashed_password)

                is_valid = password_correct

                if not password_correct:
                    print('Password or Username error(1)\n') # misleading info
                    self.start()
            self.send_message(self.__username)
        
        else:
            print('Password or Username error(2)\n')
            self.start()
        


    def send_message(self,msg):
        #!/usr/bin/env python3
        # Reference: https://realpython.com/python-sockets/
        # Documentation: https://docs.python.org/3/library/socket.html
        HOST = input("Enter IP address of server: ")

        # HOST = "127.0.0.1" # The server's hostname or IP address.
        PORT = 65000         # The port used by the server.
        ADDRESS = (HOST, PORT)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print("Connecting to {}...".format(ADDRESS))
            s.connect(ADDRESS)
            print("Busy")

            while True:
                message = msg                               
                s.sendall(message.encode())
                data = s.recv(4096)

                if(data.decode('UTF-8')=="logout"):
                    print("Received {} bytes of data decoded to: '{}'".format(
                    len(data), data.decode()))
                    break
                
            
            print("Disconnecting from server.")
        print("Done.")

