#!/usr/bin/env python3
import socket as s
import time
#import urllib3
import sys, os
#sys.path.insert(0, os.path.abspath('..'))
import subprocess
import random
import numpy as np
import datetime


#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def sendData(timestamp, data, channel, fs):
   ##### Global veriables #########
   unit = "be:lt:00.00:00:00"
   url = "https://sensorweb.us:8086"
   db = "testdb"
   user = "test"
   passw = "sensorweb"
   verbose = True

   http_post  = "curl -s -POST \'"+ url+"/write?db="+db+"\' -u "+ user+":"+ passw+" --data-binary \' "
   for value in data:
      http_post += "\n" + "beltsensor" +",location=" + unit + " "
      http_post += channel + "=" + str(value) + " " + str(int(timestamp*10e8))
      timestamp +=  1/fs # ??sampling rate is 1000Hz, not 100Hz as pi shake
   http_post += "\'  &"
   if (verbose):   
      print(http_post)
   subprocess.call(http_post, shell=True)

def read_next(fs):
    data1 = np.random.randint(10, 20, size=fs)
    data2 = np.random.randint(20, 30, size=fs)
    data3 = np.random.randint(30, 40, size=fs)
    time.sleep(1) # sleep one second
    return data1, data2, data3

if __name__ == '__main__':
   #  if len(sys.argv) <= 4:
   #      print("Example: " + sys.argv[0] + " https://sensorweb.us:8086 testdb test sensorweb")
   #      print('open browser with user/password:guest/sensorweb_guest to \
   #          see waveform at grafana: https://sensorweb.us:3000/d/Yvx-ULCWz/simsensor?orgId=1&refresh=5s')
   #      sys.exit()
   print('open browser with user/password:guest/sensorweb_guest to see waveform at grafana: https://sensorweb.us:3000/d/Yvx-ULCWz/simsensor?orgId=1&refresh=5s')
   fs = 200
   while(True):
      data1, data2, data3 = read_next(fs)
      timestamp = datetime.datetime.now().timestamp()
      sendData(timestamp, data1, "HR", fs)
      sendData(timestamp, data2, "RR", fs)
      sendData(timestamp, data3, "SR", fs)

#    start(sys.argv[1], sys.argv[2])
