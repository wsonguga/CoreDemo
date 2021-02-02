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

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#    s = socket(AF_INET, SOCK_DGRAM)
    s.bind((host,port))

    print ("Server Started.")

    while True:
        data, addr = s.recvfrom(1024)
        data = data.decode()
        print ("message from: ", str(addr))
        print ("from connect user: ", str(data))
        data = str(data).upper()
        print ("sending: " , str(data))
        s.sendto(data.encode(), addr)

    s.close()

#main function
if __name__ == "__main__":
    Main()
