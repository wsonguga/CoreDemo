#!/usr/bin/env python2.7

import socket

def Main():
    host = '127.0.0.1'
    port = 5000

#    server = (host, port)

#    s = socket.socket() # no parameter will default to TCP socket, same as below
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    message = raw_input("-> ")
    while message != 'q':
        s.send(message)
        data, addr = s.recvfrom(1024)
        print "Received from server: " + str(data)
        message = raw_input("-> ")

    s.close()

#main function
if __name__ == "__main__":
    Main()
