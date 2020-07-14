#!/usr/bin/python3
import time
import math
import datetime
import subprocess
import sys

if len(sys.argv) <= 4:
        print("Example: " + sys.argv[0] + " 3.136.84.223:57129 testdb test sensorweb")
        print("open browser with user/password:guest/sensorweb_guest to see waveform \
            at grafana: http://3.136.84.223:3000/d/Vv7164WMz/vital-signs?orgId=1&from=now-5m&to=now&refresh=5s")
        sys.exit()

f_sampling = 10
f_wave = 1
timestamp = datetime.datetime.now().timestamp()

while True:
    # IP:port, databaseName, user, password
    http_post = "curl -i -XPOST \'http://%s/write?db=%s\' -u %s:%s --data-binary \'" % (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    for i in range(f_sampling):
        timestamp += 1 / f_sampling
        value = math.sin(2 * math.pi * f_wave * timestamp)
        http_post += "\ncheckme,location=E7:CC:E2:D0:5C:C5 spo2=" 
        http_post += str(value) + " " + str(int(timestamp*10e8))
        time.sleep(1 / f_sampling)
    http_post += "\'"
    print(http_post)
    subprocess.call(http_post, shell=True)
    
    http_post = "curl -i -XPOST \'http://%s/write?db=%s\' -u %s:%s --data-binary \'" % (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    for i in range(f_sampling):
        timestamp += 1 / f_sampling
        value = math.sin(2 * math.pi * f_wave * timestamp)
        http_post += "\ncheckme,location=E7:CC:E2:D0:5C:C5 hr="
        http_post += str(value) + " " + str(int(timestamp*10e8))
        time.sleep(1 / f_sampling)
    http_post += "\'"
    print(http_post)
    subprocess.call(http_post, shell=True)
       
    http_post = "curl -i -XPOST \'http://%s/write?db=%s\' -u %s:%s --data-binary \'" % (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    for i in range(f_sampling):
        timestamp += 1 / f_sampling
        value = math.sin(2 * math.pi * f_wave * timestamp)
        http_post += "\ncheckme,location=E7:CC:E2:D0:5C:C5 rr="
        http_post += str(value) + " " + str(int(timestamp*10e8))
        time.sleep(1 / f_sampling)
    http_post += "\'"
    print(http_post)
    subprocess.call(http_post, shell=True)
          
    http_post = "curl -i -XPOST \'http://%s/write?db=%s\' -u %s:%s --data-binary \'" % (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    for i in range(f_sampling):
        timestamp += 1 / f_sampling
        value = math.sin(2 * math.pi * f_wave * timestamp)
        http_post += "\ncheckme,location=E7:CC:E2:D0:5C:C5 temperature="
        http_post += str(value) + " " + str(int(timestamp*10e8))
        time.sleep(1 / f_sampling)
    http_post += "\'"
    print(http_post)
    subprocess.call(http_post, shell=True)

