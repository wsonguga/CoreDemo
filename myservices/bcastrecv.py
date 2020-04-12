#!/usr/bin/env python2.7
# Recv UDP packets at UDP port# MYPORTS

import commands

MYPORT = 50000
BUFSIZE = 1024

import sys, time
from socket import *

# myip = commands.getoutput("hostname -I")
# print myip

s = socket(AF_INET, SOCK_DGRAM)
s.bind(('', MYPORT))
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

while 1:

    data, addr = s.recvfrom(BUFSIZE)
	print 'server received %r from %r' % (data, addr)
  
