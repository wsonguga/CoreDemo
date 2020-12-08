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

from util import local_time_epoch
from util import write_influx

verbose = False

if len(sys.argv) >= 8:
    ip = sys.argv[1]
    db = sys.argv[2]
    user = sys.argv[3]
    passw = sys.argv[4]
    unit = sys.argv[5]
    start = local_time_epoch(sys.argv[6], "America/New_York")
    end = local_time_epoch(sys.argv[7], "America/New_York")
else:
    print("Example: " + sys.argv[0] + " https://sensorweb.us testdb test sensorweb aa:bb:cc:dd:ee:ff 2020-08-13T02:03:00.200 2020-08-13T02:08:00.030")
    print("Change aa:bb:cc:dd:ee:ff to your fi:rs:tl:as:tn:am to avoid overwrite each other")
    sys.exit()

dest = {'ip': ip, 'db': db, 'user':user, 'passw':passw}

url = ip + ":3000/d/Vv7164WMz/vital-signs?orgId=1&refresh=5s&var-unit=" + unit
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
    write_influx(dest, unit, 'labeled', 'S', S, timestamp, fs)
    write_influx(dest, unit, 'labeled', 'D', D, timestamp, fs)
    write_influx(dest, unit, 'labeled', 'H', H, timestamp, fs)
    write_influx(dest, unit, 'labeled', 'R', R, timestamp, fs)

    # user your first name as the unit name or location tag if you are in a class and want to avoid overwriting with each other
    write_influx(dest, unit, 'predicted', 'S', S+random.randint(1,3), timestamp, fs)
    write_influx(dest, unit, 'predicted', 'D', D+random.randint(1,3), timestamp, fs)
    write_influx(dest, unit, 'predicted', 'H', H+random.randint(1,3), timestamp, fs)
    write_influx(dest, unit, 'predicted', 'R', R+random.randint(1,3), timestamp, fs)

    print("start:", (datetime.fromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M:%S.%f')), "end:", (datetime.fromtimestamp(timestamp+n).strftime('%Y-%m-%dT%H:%M:%S.%f')))

    # time.sleep(n) # sleep n seconds, which can be removed
    timestamp = timestamp + n # add n seconds



