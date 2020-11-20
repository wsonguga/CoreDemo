#!/usr/bin/env python3

import time
import math
import datetime
import subprocess
import sys
import random
import webbrowser
import numpy as np

verbose = True

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


if len(sys.argv) >= 6:
    ip = sys.argv[1]
    db = sys.argv[2]
    user = sys.argv[3]
    passw = sys.argv[4]
    unit = sys.argv[5]
else:
    print("Example: " + sys.argv[0] + " https://sensorweb.us:8086 testdb test sensorweb aa:bb:cc:dd:ee:ff")
    sys.exit()

url = "https://sensorweb.us:3000/d/Vv7164WMz/vital-signs?orgId=1&refresh=5s&from=now-2m&to=now&var-unit=" + unit
print("Click here to see the results in Grafana:\n\n" + url)
#  input("Press any key to continue")
webbrowser.open(url, new=2)

while True:
    timestamp = datetime.datetime.now().timestamp() # here
    
    fs = 1 # 1Hz
    n = 60 
    # spo2 = np.random.randint(80, 100, n)
    systolic = np.random.randint(100, 150, n)
    diastolic = np.random.randint(70, 90, n)
    heartrate = np.random.randint(60, 100, n)
    respiratoryrate = np.random.randint(10, 30, n)

    # user your first name as the unit name or location tag if you are in a class and want to avoid overwriting with each other
    writeInflux("predicted", "systolic", systolic, timestamp, fs, unit)
    writeInflux("predicted", "diastolic", diastolic, timestamp, fs, unit)
    writeInflux("predicted", "heartrate", heartrate, timestamp, fs, unit)
    writeInflux("predicted", "respiratoryrate", respiratoryrate, timestamp, fs, unit)

    # user your first name as the unit name or location tag if you are in a class and want to avoid overwriting with each other
    writeInflux("labeled", "systolic", systolic, timestamp, fs, unit)
    writeInflux("labeled", "diastolic", diastolic, timestamp, fs, unit)
    writeInflux("labeled", "heartrate", heartrate, timestamp, fs, unit)
    writeInflux("labeled", "respiratoryrate", respiratoryrate, timestamp, fs, unit)

    time.sleep(60) # sleep 60 seconds


#     # https://ip:port, databaseName, user, password
#     http_post = "curl -i -XPOST \'%s/write?db=%s\' -u %s:%s --data-binary \'" % (ip, db, user, password)
#     timestamp = str(int(now*10e8))
#     http_post += "\nvital,location=%s spo2=%d,systolic=%d,diastolic=%d,heartrate=%d,respiratoryrate=%d" %(mac, spo2, systolic, diastolic, heartrate, respiratoryrate)
#     http_post += " " + timestamp
#     http_post += "\'"
#     print(http_post)
#     subprocess.call(http_post, shell=True)



