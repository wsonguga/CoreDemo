#!/usr/bin/env python3

import socket

def Main():
    host = '0.0.0.0' # allow to connect to any other network computer
    port = 5002

    server = ('127.0.0.1', 5001)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host,port))

    message = input("-> ")
    while message != 'q':
        s.sendto(message.encode(), server)
        data, addr = s.recvfrom(1024)
        print ("Received from server: " + str(data.decode()))
        message = input("-> ")

    s.close()

#main function
if __name__ == "__main__":
    Main()
