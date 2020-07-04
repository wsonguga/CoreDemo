#!/usr/bin/env python2.7

import socket

def Main():
    host = '0.0.0.0' # allow to connect to any other network computer
    port = 5001

    server = ('127.0.0.1', 5000)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host,port))

    message = raw_input("-> ")
    while message != 'q':
        s.sendto(message, server)
        data, addr = s.recvfrom(1024)
        print "Received from server: " + str(data)
        message = raw_input("-> ")

    s.close()

#main function
if __name__ == "__main__":
    Main()
