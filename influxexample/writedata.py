#!/usr/bin/env python3
import time
import math
import datetime
import subprocess
import sys

if len(sys.argv) <= 4:
        print("Example: " + sys.argv[0] + " https://sensorweb.us:8086 testdb test sensorweb")
        print('open browser with user/password:guest/sensorweb_guest to \
            see waveform at grafana: https://sensorweb.us:3000/d/Yvx-ULCWz/simsensor?orgId=1&refresh=5s')
        sys.exit()

f_sampling = 10
f_wave = 1
timestamp = datetime.datetime.now().timestamp()

while True:
    # IP:port, databaseName, user, password
    http_post = "curl -i -XPOST \'%s/write?db=%s\' -u %s:%s --data-binary \'" % (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    for i in range(f_sampling):
        timestamp += 1 / f_sampling
        value = math.sin(2 * math.pi * f_wave * timestamp)
        http_post += "\nsimsensor,location=UGA temperature=" 
        # if you have other sensor readings, just change 'temperature' to other sensor names such as 'humidity', 'co2', etc
        http_post += str(value) + " " + str(int(timestamp*10e8))
        time.sleep(1 / f_sampling)
    http_post += "\'"
    print(http_post)
    subprocess.call(http_post, shell=True)

