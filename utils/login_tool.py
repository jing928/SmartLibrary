"""
This module provides a helper tool to send message using sockets
"""

import socket


class LoginTool:
    """
    LoginTool provides method to handle communication between server and client using
    sockets
    """

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
