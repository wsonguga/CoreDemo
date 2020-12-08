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
from util import read_influx

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

src = {'ip': ip, 'db': db, 'user':user, 'passw':passw}

url = ip + ":3000/d/Vv7164WMz/vital-signs?orgId=1&refresh=5s&var-unit=" + unit
url = url + "&from=" + str(int(start*1000)) #+ "000" 
url = url + "&to=" + str(int(end*1000)) #+ "000"

print("Click here to see the results in Grafana (user/password:viewer/guest):\n" + url)
# input("Press any key to continue")
# webbrowser.open(url, new=2)

vitals = ['H', 'R', 'S', 'D']
n = 10

for vital in vitals:
    data_labeled, times_labeled = read_influx(src, unit, 'labeled', vital, start, end)
    data_predicted, times_predicted = read_influx(src, unit, 'predicted', vital, start, end)
    # data_labeled =     np.random.randint(100, 150, n) # [1, 2, 3, 4, 5]
    # data_predicted =   np.random.randint(50, 100, n) # [2, 3, 4, 5, 4]
    print ("MAE (" + vital + "):", np.mean(np.abs(data_labeled - data_predicted)) )
