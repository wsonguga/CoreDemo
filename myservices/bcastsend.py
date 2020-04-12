#!/usr/bin/env python2.7
# Broadcast UDP packets to 1-hop neighbors at UDP port# MYPORTS

import commands
import time as time

MYPORT = 50000

import sys, time
from socket import *

# myip = commands.getoutput("hostname -I")
# print myip

if(len(sys.argv)<2):
  print 'Usage: ./bcastsend.py x.x.0.0 \n where x.x is the subnet address'
  sys.exit()

s = socket(AF_INET, SOCK_DGRAM)
s.bind(('', MYPORT))
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

k = 0

while 1:
    data = 'Iteration: ' + str(k) + ' '  + repr(time.time()) + '\n'
    s.sendto(data, (sys.argv[1], MYPORT))

    print 'server sent %r to %r' % (data, sys.argv[1])

    k = k + 1

    
