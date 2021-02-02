#!/usr/bin/env python3

import socket

def Main():
    host = '127.0.0.1'
    port = 5001

#    server = (host, port)

#    s = socket.socket() # no parameter will default to TCP socket, same as below
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    message = input("-> ")
    print(message)
    while message != 'q':
        s.send(message.encode())
        data = s.recv(1024)
        print ("Received from server: " + data.decode())
        message = input("-> ")

    s.close()

#main function
if __name__ == "__main__":
    Main()
