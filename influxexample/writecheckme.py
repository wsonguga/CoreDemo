#!/usr/bin/python3
import time
import math
import datetime
import subprocess
import sys
import random


if len(sys.argv) <= 4:
        print("Example: " + sys.argv[0] + " 3.136.84.223:8086 testdb test sensorweb")
        print("open browser with user/password:guest/sensorweb_guest to see waveform \
            at grafana: http://3.136.84.223:3000/d/Vv7164WMz/vital-signs?orgId=1&from=now-5m&to=now&refresh=5s")
        sys.exit()

f_sampling = 10
f_wave = 1

ip = sys.argv[1]
db = sys.argv[2]
user = sys.argv[3]
password = sys.argv[4]

while True:
    now = datetime.datetime.now().timestamp()
    # IP:port, databaseName, user, password
    http_post = "curl -i -XPOST \'http://%s/write?db=%s\' -u %s:%s --data-binary \'" % (ip, db, user, password)
    for i in range(f_sampling):
        timestamp = now + i / f_sampling
        value = math.sin(2 * math.pi * f_wave * timestamp)
        http_post += "\ncheckme,location=E7:CC:E2:D0:5C:C5 spo2=" 
        http_post += str(value) + " " + str(int(timestamp*10e8))
    http_post += "\'"
    print(http_post)
    subprocess.call(http_post, shell=True)
    
    http_post = "curl -i -XPOST \'http://%s/write?db=%s\' -u %s:%s --data-binary \'" % (ip, db, user, password)
    for i in range(f_sampling):
        timestamp = now + i / f_sampling
        value = math.sin(2 * math.pi * f_wave * timestamp)
        http_post += "\ncheckme,location=E7:CC:E2:D0:5C:C5 hr="
        http_post += str(value) + " " + str(int(timestamp*10e8))
        # time.sleep(1 / f_sampling)
    http_post += "\'"
    print(http_post)
    subprocess.call(http_post, shell=True)
       
    http_post = "curl -i -XPOST \'http://%s/write?db=%s\' -u %s:%s --data-binary \'" % (ip, db, user, password)
    for i in range(f_sampling):
        timestamp = now + i / f_sampling
        value = math.sin(2 * math.pi * f_wave * timestamp)
        http_post += "\ncheckme,location=E7:CC:E2:D0:5C:C5 rr="
        http_post += str(value) + " " + str(int(timestamp*10e8))
    http_post += "\'"
    print(http_post)
    subprocess.call(http_post, shell=True)
          
    http_post = "curl -i -XPOST \'http://%s/write?db=%s\' -u %s:%s --data-binary \'" % (ip, db, user, password)
    for i in range(f_sampling):
        timestamp = now + i / f_sampling
        value = random.randint(35, 43)#math.sin(2 * math.pi * f_wave * timestamp)
        http_post += "\ncheckme,location=E7:CC:E2:D0:5C:C5 temperature="
        http_post += str(value) + " " + str(int(timestamp*10e8))
    http_post += "\'"
    print(http_post)
    subprocess.call(http_post, shell=True)

    time.sleep(1)


