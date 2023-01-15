#!/usr/bin/env python3
import socket
from datetime import datetime
from time import sleep
import random

#from socket import *

def read_next():
    utc_time = datetime.utcnow()
    epoch_time = (utc_time - datetime(1970, 1, 1)).total_seconds()
    data = "{'Z'," + str(epoch_time)
    for x in range(100): # 100 sample each read
        data = data + "," + str(x) # str(random.randrange(0, 65535))
    data = data + "}"
    sleep(1) # sleep one second
    return data

def Main():
    host = '127.0.0.1'
    port = 8888

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#    s = socket(AF_INET, SOCK_DGRAM)
    s.bind((host,port))

    print ("Server Started at " + host + ":" + str(port) +".")

    data, addr = s.recvfrom(1024)
    print ("message from: ", str(addr))
    print ("from connect user: ", str(data))


# The output format is straightforward:
# Each data packet contains data for a single channel only
# Entire data packet is wrapped with open and closing braces: { }
# All fields are separated by a comma
# First element defines the channel name - string in single quotes
# Second element defines the timestamp, in epoch seconds, down to milliseconds, of the first data point - float
# All remaining elements are the data points themselves - integer
# Rate of Data Packet Transmission - can be calculated from the timestamps of two subsequent packets for the same channel
# Sample Rate - can be obtained by counting the data points of a single data packet, in conjunction with the derived data packet transmission rate
# Example: {'SHZ', 1507760140.530, 614, 916, 1095, 1156, 839, 923, 861, 856, 861, 789, 568, 823, 965, 788, 835, 991, 1028, 1225, 1142, 828, 682, 635, 771, 978, 834, 1167, 1116, 888, 627, 564, 944, 994, 780, 652, 811, 915, 832, 1134, 1020, 594, 756, 782, 748, 810, 864, 936, 977, 1014, 676, 502}
    while True:
        #data = "{'Z', 1507760140.530, 614, 916, 1095, 1156, 839, 923, 861, 856, 861, 789, 568, 823, 965, 788, 835, 991, 1028, 1225, 1142, 828, 682, 635, 771, 978, 834, 1167, 1116, 888, 627, 564, 944, 994, 780, 652, 811, 915, 832, 1134, 1020, 594, 756, 782, 748, 810, 864, 936, 977, 1014, 676, 502}"
        data = read_next()
        print ("sending: " , data)
        byte_message = bytes(data, "utf-8")
        sent = s.sendto(byte_message, addr)
        if sent == 0:
                raise RuntimeError("socket connection broken")

    s.close()

#main function
if __name__ == "__main__":
    Main()