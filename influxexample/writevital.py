#!/usr/bin/env python3

import time
import math
import subprocess
import sys
import random
import webbrowser
import numpy as np
from datetime import datetime
from dateutil import tz
import pytz


verbose = False


def localTimeToEpoch(time, zone):
    local_tz = pytz.timezone(zone)
    localTime = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%f")
    local_dt = local_tz.localize(localTime, is_dst=None)
    # utc_dt = local_dt.astimezone(pytz.utc)
    epoch = local_dt.timestamp()
    print("epoch time:", epoch) # this is the epoch time in seconds, times 1000 will become epoch time in milliseconds
    return epoch 

# dataname - the dataname such as temperature, heartrate, etc
# timestamp - the timestamp (in second) of the first element in the data array, such as datetime.datetime.now().timestamp()
def writeInflux(tablename, dataname, data, timestamp, fs, unit):
   http_post  = "curl -s -POST \'"+ ip+"/write?db="+db+"\' -u "+ user+":"+ passw+" --data-binary \' "
   for value in data:
      http_post += "\n" + tablename +",location=" + unit + " "
      http_post += dataname + "=" + str(value) + " " + str(int(timestamp*10e8))
      timestamp +=  1/fs
   http_post += "\'  &"
   if (verbose):   
      print(http_post)
   subprocess.call(http_post, shell=True)


if len(sys.argv) >= 8:
    ip = sys.argv[1]
    db = sys.argv[2]
    user = sys.argv[3]
    passw = sys.argv[4]
    unit = sys.argv[5]
    start = localTimeToEpoch(sys.argv[6], "America/New_York")
    end = localTimeToEpoch(sys.argv[7], "America/New_York")
else:
    print("Example: " + sys.argv[0] + " https://sensorweb.us:8086 testdb test sensorweb aa:bb:cc:dd:ee:ff 2020-08-13T02:03:00.200 2020-08-13T02:08:00.030")
    print("Change aa:bb:cc:dd:ee:ff to your fi:rs:tl:as:tn:am to avoid overwrite each other")
    sys.exit()

url = "https://sensorweb.us:3000/d/Vv7164WMz/vital-signs?orgId=1&refresh=5s&var-unit=" + unit
url = url + "&from=" + str(int(start*1000)) #+ "000" 
url = url + "&to=" + str(int(end*1000)) #+ "000"

print("Click here to see the results in Grafana (user/password:viewer/guest):\n" + url)
#  input("Press any key to continue")
webbrowser.open(url, new=2)

# timestamp = datetime.now().timestamp() # here

timestamp = start
while timestamp < end:
    print("epoch time:", timestamp) 
    fs = 1 # 1Hz
    n = 60 # write n seconds data at one time. for example, fs =1 and n = 60 means 60 seconds data and 1 per second to write at once 
    S = np.random.randint(100, 150, n)
    D = np.random.randint(70, 90, n)
    H = np.random.randint(60, 100, n)
    R = np.random.randint(10, 30, n)

    # user your first name as the unit name or location tag if you are in a class and want to avoid overwriting with each other
    writeInflux("labeled", "S", S, timestamp, fs, unit)
    writeInflux("labeled", "D", D, timestamp, fs, unit)
    writeInflux("labeled", "H", H, timestamp, fs, unit)
    writeInflux("labeled", "R", R, timestamp, fs, unit)

    # user your first name as the unit name or location tag if you are in a class and want to avoid overwriting with each other
    writeInflux("predicted", "S", S+random.randint(1,3), timestamp, fs, unit)
    writeInflux("predicted", "D", D+random.randint(1,3), timestamp, fs, unit)
    writeInflux("predicted", "H", H+random.randint(1,3), timestamp, fs, unit)
    writeInflux("predicted", "R", R+random.randint(1,3), timestamp, fs, unit)

    print("start:", (datetime.fromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M:%S.%f')), "end:", (datetime.fromtimestamp(timestamp+n).strftime('%Y-%m-%dT%H:%M:%S.%f')))

    # time.sleep(n) # sleep n seconds, which can be removed
    timestamp = timestamp + n # add n seconds



