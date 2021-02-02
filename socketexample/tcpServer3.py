#!/usr/bin/env python3
import socket
#from socket import *

def Main():
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
#    host = '127.0.0.1'
    host = ''
    port = 5001

#    s = socket.socket() # no parameter will default to TCP socket, same as below
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    s = socket(AF_INET, SOCK_DGRAM)
    s.bind((host,port))

    print ("Server Started.")

    s.listen(1)
    c, addr = s.accept()
    print ("Connection from: ", str(addr))
    while True:
        data, addr = c.recvfrom(1024)
        data = data.decode()
        if not data:
            break
        print ("message from: ", str(addr))
        print ("from connect user: ", str(data))
        data = str(data).upper()
        print ("sending: " , str(data))
        c.send(data.encode())

    c.close()

#main function
if __name__ == "__main__":
    Main()
