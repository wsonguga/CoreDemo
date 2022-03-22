#!/usr/bin/env python3

from scipy.signal import butter, lfilter
from scipy import signal
from datetime import datetime, date
from influxdb import InfluxDBClient
import numpy
import random
import time
import operator
import sys, os
import logging
import algorithm as alg
#from scipy import stats
import nitime.algorithms as nt_alg
import numpy as np
from numpy import array
import scipy as sp
import threading
from datetime import datetime
from dateutil import tz
import pytz
import ast
import requests
import subprocess
from dateutil.parser import parse
#from config import Config
import webbrowser
from utils import * 

ip = "sensorweb.us"
port = "8086"
user = "test"
passw = "sensorweb"
db = "shake"

rip = ip
debug = True; #str2bool(config.get('general', 'debug'))
verbose = True

src = {'ip': 'https://sensorweb.us', 'db': 'shake', 'user':'test', 'passw':'sensorweb'}
dest = {'ip': 'https://sensorweb.us', 'db': 'algtest', 'user':'test', 'passw':'sensorweb'}

def str2bool(v):
  return v.lower() in ("true", "1", "https", "t")

########### main entrance ########
def main():
 progname = sys.argv[0]
 if(len(sys.argv)<2):
    print("Usage: %s mac [start] [end] [ip] [https/http]" %(progname))
    print("Example: %s b8:27:eb:97:f5:ac   # start with current time and run in real-time as if in a node" %(progname))
    print("Example: %s b8:27:eb:97:f5:ac 2020-08-13T02:03:00.200 # start with the specified time and run non-stop" %(progname))
    print("Example: %s b8:27:eb:97:f5:ac 2020-08-13T02:03:00.200 2020-08-13T02:05:00.030 # start and end with the specified time" %(progname))
    print("Example: %s b8:27:eb:97:f5:ac 2020-08-13T02:03:00.200 2020-08-13T02:05:00.030 sensorweb.us https # specify influxdb IP and http/https" %(progname))
    quit()

 # Parameters from Config file
 db           = 'shake' # config.get('general', 'dbraw')
 buffersize   = 60 # config.get('general', 'buffersize')
 samplingrate = 100 # int(config.get('general', 'samplingrate'))
 hrTimeWindow    = 30 # int(config.get('main', 'hrTimeWindow'))
 maxbuffersize               = int(buffersize) * int(samplingrate)
 windowSize = elementsNumberHR = hrTimeWindow * samplingrate

 # Buffers for time and
 buffer      = []
 buffertime  = []

 alg.logpath = ""
# Getting the user input parameters
 global ip, rip

 unit = sys.argv[1]

 if(len(sys.argv) > 4):
   ip = sys.argv[4] # influxdb IP address
 

 if(len(sys.argv) > 5):
    ssl = str2bool(sys.argv[5]) #https or http
    httpStr = sys.argv[5]+"://"
 else:
    ssl = True
    httpStr = "https://"

 if(len(sys.argv) > 2):
    current = local_time_epoch(sys.argv[2], "America/New_York")

 else:
    current = datetime.utcnow().timestamp()
    bDependOnMovement = True

 if(len(sys.argv) > 3):
     endSet = True
     end = local_time_epoch(sys.argv[3], "America/New_York")

 else:
     endSet = False
     end = datetime.utcnow().timestamp() # never will be used, just give a value to avoid compile errors

 endEpoch = end # int( (end - datetime(1970,1,1)).total_seconds())

# Determining the starting point of the buffer using epoch time
 epoch2 = current # int( (current - datetime(1970,1,1)).total_seconds())
 startEpoch = epoch2

 print("len(sys.argv)", len(sys.argv))
 print("### Current time:", current, " ### \n")
 print("### End time:", end, " ### \n")
 url = httpStr + rip + ":3000/d/o2RBARGMz/bed-dashboard-algtest?var-mac=" + str(unit)

 if(len(sys.argv) > 2):
    url = url + "&from=" + str(int(startEpoch*1000)) #+ "000" 
 else:
    url = url + "&from=now-2m"

 if(len(sys.argv) > 3):
    url = url + "&to=" + str(int(endEpoch*1000)) #+ "000"
 else:
    url = url + "&to=now"
 name = 'vitalsigns'
 url = url + f"&var-name={name}&orgId=1&refresh=3s"


 print("Click here to see the results in Grafana:\n\n" + url)
#  input("Press any key to continue")
 webbrowser.open(url, new=2)


 # Parameters for the Query
 epoch2 = epoch2 - 1
 epoch1 = epoch2 - 1

 try:
   client = InfluxDBClient(ip, port, user, passw, db, ssl)
 except Exception as e:
   print("main(), DB access error:")
   print("Error", e)
   quit()


 # set max retries for DB query
 numTry = 0 
 MAXTRY = 100 # max try of 100 seconds
 result = []
 # Infinite Loop
 while True:
    # Cheking is the process need to sleep
    current = datetime.utcnow().timestamp() #(datetime.utcnow() - datetime(1970,1,1)).total_seconds()
    epoch2 = epoch2 + 1
    epoch1 = epoch1 + 1
    if (endSet == False and (current-epoch2) < 1): 
        time.sleep(1)
        if(debug): print("*********")

#    if(debug): print("*****************************************"+str(statusKey))
    if (endSet and epoch2 > endEpoch):
        if(debug): print("**** Ended as ", epoch2, " > ", end, " ***")
        print("Click here to see the results in Grafana:\n\n" + url)
        quit()
    
    print('start:', epoch1, 'end:', epoch2)
    
    try:
        values, times = read_influx(src, unit, 'Z', 'value', epoch1, epoch2)
    except Exception as e:
        print("main(), no data in the query time period:")
        print("Error", e)
        time.sleep(1)
        numTry += 1
        if (numTry > MAXTRY):            
            quit()

    # query = 'SELECT "value" FROM Z WHERE ("location" = \''+unit+'\')  and time >= '+ str(int(epoch1*10e8))+' and time <= '+str(int(epoch2*10e8))
    # print(query)

    # try:
    #     result = client.query(query)
    # except Exception as e:
    #     print("main(), no data in the query time period:")
    #     print("Error", e)
    #     time.sleep(1)
    #     numTry += 1
    #     if (numTry > MAXTRY):            
    #         quit()
    # # print(result)
    # points = list(result.get_points())
    # values =  list(map(operator.itemgetter('value'), points))
    # times  =  list(map(operator.itemgetter('time'),  points))

    # the buffer management modules
    buffertime = buffertime + times
    buffer     = buffer + values
    buffLen    = len(buffer)
    if(debug): 
        print("buffLen: ", buffLen) 
        if(buffLen>0):
            print("Buffer Time:    " + buffertime[0]+ "  -   " + buffertime[buffLen-1])
            # print("Buffer Time:    " + epoch_time_local(buffertime[0], "America/New_York") + "  -   " + epoch_time_local(buffertime[buffLen-1], "America/New_York"))
    #  Cutting the buffer when overflow
    if(buffLen > maxbuffersize):
       difSize = buffLen - maxbuffersize
       del buffer[0:difSize]
       del buffertime[0:difSize]
       buffLen    = buffLen - difSize
    # get more data if the buffer does not have enough data for the minimum window size
    if (buffLen < windowSize):
        continue
    
    data = buffer[buffLen-windowSize:buffLen]
    nowtime = buffertime[buffLen-1]

    #  the blood pressure estimation algorithm
    if(debug): print("Calculating vital signs")
    hr,rr,bph,bpl = alg.predict(data, fs=100, cutoff=4,nlags=200,order=1)
    if(debug): print('hr:', hr, ' rr:', rr, ' bph:', bph, ' bpl:', bpl)

    fs = 1
    print('nowtime:', nowtime)
    timestamp = local_time_epoch(nowtime[:-1], "UTC")
    write_influx(dest, unit, name, 'heartrate', hr, timestamp, fs)
    write_influx(dest, unit, name, 'respiratoryrate', rr, timestamp, fs)
    write_influx(dest, unit, name, 'systolic', bph, timestamp, fs)
    write_influx(dest, unit, name, 'diastolic', bpl, timestamp, fs)
    # end of adding

if __name__== '__main__':
  main()
