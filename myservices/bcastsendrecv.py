#!/usr/bin/env python2.7
# Broadcast & Receive UDP packets to & from 1-hop neighbors at UDP port# MYPORTS

import commands
import time as time

MYPORT = 50000
BUFSIZE = 1024
TIMEOUT = 2.0 # 2 seconds

import sys, time
from socket import *

# myip = commands.getoutput("hostname -I")
# print myip

if(len(sys.argv)<2):
  print 'Usage: ./bcastsendrecv.py x.x.0.0 \n where x.x is the subnet address'
  sys.exit() 

s = socket(AF_INET, SOCK_DGRAM)
s.bind(('', MYPORT))
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
s.settimeout(TIMEOUT)

k = 0

while 1:
    data = 'Iteration: ' + str(k) + ' '  + repr(time.time()) + '\n'
    s.sendto(data, (sys.argv[1], MYPORT))

    print 'server sent %r to %r' % (data, sys.argv[1])

    while 1:
        try:
            data, addr = s.recvfrom(BUFSIZE)
        except timeout:
            break
        ip, port = addr
        print 'received %r from %r' % (data, ip)

    k = k + 1

    
