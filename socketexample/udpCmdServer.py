#!/usr/bin/env python2.7
import socket
#from socket import *
import commands

def Main():
    host = '127.0.0.1'
    port = 5000
	
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#    s = socket(AF_INET, SOCK_DGRAM)
    s.bind((host,port))

    print ("Server Started.")

    while True:
        data, addr = s.recvfrom(1024)
        print "message from: ", str(addr)
        print "from connect user: ", str(data)
        status, output = commands.getstatusoutput(str(data))
#        data = str(data).upper()

        print "sending: " , output
        s.sendto(str(output), addr)

    s.close()
    
#main function
if __name__ == "__main__":
    Main()
