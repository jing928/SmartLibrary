#!/usr/bin/env python3
# Reference: https://realpython.com/python-sockets/
# Documentation: https://docs.python.org/3/library/socket.html

import socket

HOST = ""    # Empty string means to listen on all IP's on the machine, also works with IPv6.
             # Note "0.0.0.0" also works but only with IPv4.
PORT = 65000 # Port to listen on (non-privileged ports are > 1023).
ADDRESS = (HOST, PORT)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(ADDRESS)
    s.listen()

    print("Listening on {}...".format(ADDRESS))
    conn, addr = s.accept()
    with conn:
        print("Connected to {}".format(addr))

        while True:
            data = conn.recv(4096)
            if(not data):
                break
            print("User: '{}' log in successfully!".format(data.decode()))
            # print("Sending data back.")
            # conn.sendall(data)
            msg = input("Please input a reply message (logout):\n")
            conn.sendall(msg.encode())
        
        print("Disconnecting from client.")
    print("Closing listening socket.")
print("Done.")
