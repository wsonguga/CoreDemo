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

ip = "sensorweb.us"
port = "8086"
user = "test"
passw = "sensorweb"
db = "shake"
rip = ip
rport = port
ruser = user
rpassw = passw
rdb = "algtest"

# define functions here
def utcToLocalTime(time2, formatt, from_zone, to_zone):
    utc = datetime.strptime(time2, formatt)
    utc = utc.replace(tzinfo=from_zone)
    central = utc.astimezone(to_zone)
    timeDetected = central.strftime("%m-%d %I:%M %p")
    return timeDetected

def localTimeToUTC(time):
    local_tz = pytz.timezone("America/New_York")
    localTime = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%f")
    local_dt = local_tz.localize(localTime, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    print("epoch time with tzinfo:", str(utc_dt))
    utc_dt = utc_dt.replace(tzinfo=None)
    print("local time:",local_dt)
    print("UTC time:", utc_dt)
    # epoch = int( (utc_dt - datetime(1970,1,1)).total_seconds())
    # epoch = int(utc_dt.timestamp()*1000)
    epoch = int(local_dt.timestamp()*1000)

    print("epoch time:", str(epoch))
    return epoch # utc_dt

def saveResults(unit, serie, field, value, time):
   time = time[0:19]

   utc_time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
   epoch_time = int((utc_time - datetime(1970, 1, 1)).total_seconds())

   http_post2 = "curl -s -POST --insecure \'https://"+rip+":"+rport+"/write?db="+rdb+"\' -u "+ruser+":"+rpassw+" --data-binary \' "
   http_post2 += "\n"+serie+",location="+unit+" "+field+"="+value+" "+str(epoch_time)+"000000000"
   http_post2 += "\'  &"

   subprocess.call(http_post2, shell=True)

def str2bool(v):
  return v.lower() in ("true", "1", "https", "t")

########### main entrance ########
def main():
 progname = sys.argv[0]
 if(len(sys.argv)<2):
    print("Usage: %s mac [start] [end] [ip] [https/http]" %(progname))
    print("Example: %s b8:27:eb:97:f5:ac   # start with current time and run in real-time as if in a node" %(progname))
    print("Example: %s b8:27:eb:97:f5:ac 2020-08-13T05:27:00.000 # start with the specified time and run non-stop" %(progname))
    print("Example: %s b8:27:eb:97:f5:ac 2020-08-13T05:27:00.000 2020-08-13T05:29:00.000 # start and end with the specified time" %(progname))
    print("Example: %s b8:27:eb:97:f5:ac 2020-08-13T05:27:00.000 2020-08-13T05:29:00.000 sensorweb.us https # specify influxdb IP and http/https" %(progname))
    quit()

#  formatt = '%Y-%m-%dT%H:%M:%S.%fZ'
#  from_zone = tz.tzutc()
#  to_zone = pytz.timezone("America/New_York")

 # Parameters from Config file
 debug = False; #str2bool(config.get('general', 'debug'))
 db           = 'shake' # config.get('general', 'dbraw')
 buffersize   = 60 # config.get('general', 'buffersize')
 samplingrate = 100 # int(config.get('general', 'samplingrate'))
 hrTimeWindow    = 30 # int(config.get('main', 'hrTimeWindow'))
 maxbuffersize               = int(buffersize) * int(samplingrate)
 windowSize = elementsNumberHR = hrTimeWindow * samplingrate

 # Buffers for time and
 buffer      = []
 buffertime  = []


#t1 = time.perf_counter()
#print("t1-t0= " +str(t1-t0))
 alg.logpath = ""
# Getting the user input parameters
 global ip, rip

 unit = sys.argv[1]

 if(len(sys.argv) > 4):
   ip = sys.argv[4] # influxdb IP address
   rip = ip
 

 if(len(sys.argv) > 5):
    ssl = str2bool(sys.argv[5]) #https or http
    httpStr = "http://"
 else:
    ssl = True
    httpStr = "https://"

 if(len(sys.argv) > 2):
    # current = datetime.strptime(sys.argv[2], "%Y-%m-%dT%H:%M:%S.%fZ") + (datetime.utcnow() - datetime.now())
#    current = datetime.strptime("2018-06-29T08:15:27.243860Z", "%Y-%m-%dT%H:%M:%S.%fZ")
    current = localTimeToUTC(sys.argv[2])

 else:
    current = datetime.utcnow()
    bDependOnMovement = True

 if(len(sys.argv) > 3):
     endSet = True
#     end = datetime.strptime('2018-06-29T08:15:27.243860', '%Y-%m-%dT%H:%M:%S.%f')
    #  end = datetime.strptime(sys.argv[3], "%Y-%m-%dT%H:%M:%S.%fZ") + (datetime.utcnow() - datetime.now())
     end = localTimeToUTC(sys.argv[3])

 else:
     endSet = False
     end = datetime.utcnow() # never will be used, just give a value to avoid compile errors

 endEpoch = end # int( (end - datetime(1970,1,1)).total_seconds())

# Determining the starting point of the buffer using epoch time
 epoch2 = current # int( (current - datetime(1970,1,1)).total_seconds())
 startEpoch = epoch2

 #current = datetime.utcnow()
#  print("len(sys.argv)", len(sys.argv))
#  print("### Current time:", current, " ### \n")
#  print("### End time:", end, " ### \n")
#  print("Click here to see the results in Grafana:\n\n" +
#               httpStr + rip + ":3000/d/o2RBARGMz/bed-dashboard-algtest?var-mac=" +
#                str(unit)+ "&orgId=1&from=" + str(startEpoch) + "000" + "&to=" + str(endEpoch) + "000")

 print("len(sys.argv)", len(sys.argv))
 print("### Current time:", current, " ### \n")
 print("### End time:", end, " ### \n")
 url = httpStr + rip + ":3000/d/o2RBARGMz/bed-dashboard-algtest?var-mac=" + str(unit)

 if(len(sys.argv) > 2):
    url = url + "&from=" + str(startEpoch) #+ "000" 
 else:
    url = url + "&from=now-2m"

 if(len(sys.argv) > 3):
    url = url + "&to=" + str(endEpoch) #+ "000"
 else:
    url = url + "&to=now"
 url = url + "&orgId=1&refresh=3s"


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
 debug = True
 # Infinite Loop
 while True:
    # Cheking is the process need to sleep
    current = int( (datetime.utcnow() - datetime(1970,1,1)).total_seconds())
    epoch2 = epoch2 + 1
    epoch1 = epoch1 + 1
    if (endSet == False and (current-epoch2) < 1):
        time.sleep(1)
        if(debug): print("*********")

#    if(debug): print("*****************************************"+str(statusKey))
    if (endSet and epoch2 > endEpoch):
        if(debug): print("**** Ended as ", epoch2, " > ", end, " ***")
        print("Click here to see the results in Grafana:\n\n" +
              httpStr + rip + ":3000/d/o2RBARGMz/bed-dashboard-algtest?var-mac=" +
               str(unit)+ "&orgId=1&from=" + str(startEpoch) + "000" + "&to=" + str(endEpoch) + "000")
        #print("The sleep monitoring result from node program is at https://sensorweb.us:3000/d/VmjKXrXWz/bed-dashboard?orgId=1&refresh=5s&var-mac=" + str(unit))
        quit()
    
    stampIni = (datetime.utcfromtimestamp(epoch1).strftime('%Y-%m-%dT%H:%M:%S.000Z'))
    stampEnd = (datetime.utcfromtimestamp(epoch2).strftime('%Y-%m-%dT%H:%M:%S.000Z'))
    #t0 = time.perf_counter()
    if(debug): print("stampIni time: " + stampIni)
    if(debug): print("stampEnd time: " + stampEnd)
    query = 'SELECT "value" FROM Z WHERE ("location" = \''+unit+'\')  and time >= \''+stampIni+'\' and time <= \''+stampEnd+'\'   '

    try:
        result = client.query(query)
    except Exception as e:
        print("main(), no data in the query time period:")
        print("Error", e)
        time.sleep(1)
        numTry += 1
        if (numTry > MAXTRY):            
            quit()

    # print(result)
    points = list(result.get_points())
    values =  list(map(operator.itemgetter('value'), points))
    times  =  list(map(operator.itemgetter('time'),  points))

    # the buffer management modules
    buffertime = buffertime + times
    buffer     = buffer + values
    buffLen    = len(buffer)
    if(debug): 
        print("buffLen: ", buffLen) 
        if(buffLen>0):
            print("Buffer Time:    " + str(buffertime[0]) + "  -   " + str(buffertime[buffLen-1]))

    # Cutting the buffer when overflow
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
    bphigh,bplow = alg.calculateVitals(data, fs=100, cutoff=4,nlags=200,order=1)
    saveResults(unit, 'bpressure', 'bph' ,str(bphigh), nowtime)
    saveResults(unit, 'bpressure', 'bpl' ,str(bplow), nowtime)
    if(debug): print("bph:", bphigh, " bpl:", bplow)
    # end of adding

if __name__== '__main__':
  main()
