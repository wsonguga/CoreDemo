#!/usr/bin/env python3

import time
import math
import datetime
import subprocess
import sys
import random

if len(sys.argv) == 1:
    ip = "https://sensorweb.us:8086"
    db = "algtest"
    user = "test"
    password = "sensorweb"
    mac = "aa:bb:cc:dd:ee:ff"
elif len(sys.argv) >= 6:
    ip = sys.argv[1]
    db = sys.argv[2]
    user = sys.argv[3]
    password = sys.argv[4]
    mac = sys.argv[5]
else:
    print("Example: " + sys.argv[0] + " https://sensorweb.us:8086 algtest test sensorweb aa:bb:cc:dd:ee:ff")
    print("open browser with user/password:guest/sensorweb_guest to see waveform \
        at grafana: https://sensorweb.us:3000/d/Vv7164WMz/vital-signs?orgId=1&from=now-5m&to=now&refresh=5s")
    sys.exit()


while True:
    now = datetime.datetime.now().timestamp()
    # https://ip:port, databaseName, user, password
    http_post = "curl -i -XPOST \'%s/write?db=%s\' -u %s:%s --data-binary \'" % (ip, db, user, password)
    timestamp = str(int(now*10e8))
    
    spo2 = random.randint(80, 100) #math.sin(2 * math.pi * f_wave * timestamp)
    systolic = random.randint(100, 150)
    diastolic = random.randint(70, 90)
    heartrate = random.randint(60, 100)
    respiratoryrate = random.randint(10, 30)
    http_post += "\nvital,location=%s spo2=%d,systolic=%d,diastolic=%d,heartrate=%d,respiratoryrate=%d" %(mac, spo2, systolic, diastolic, heartrate, respiratoryrate)
#    http_post += "\ncaretaker4,location=%s spo2=%s,systolic=%s,diastolic=%s,heartrate=%s,respiratoryrate=%s" %(mac, spo2, systolic, diastolic, heartrate, respiratoryrate)
    http_post += " " + timestamp

    # spo2 = random.randint(80, 100)
    # http_post += "\nvital,location=%s spo2=" %(mac)
    # http_post += str(spo2) + " " + timestamp

    # systolic = random.randint(100, 150)
    # http_post += "\nvital,location=%s systolic=" %(mac)
    # http_post += str(systolic) + " " + timestamp

    # diastolic = random.randint(70, 90)
    # http_post += "\nvital,location=%s diastolic=" %(mac)
    # http_post += str(diastolic) + " " + timestamp

    # heartrate = random.randint(60, 100)
    # http_post += "\nvital,location=%s heartrate=" %(mac)
    # http_post += str(heartrate) + " " + timestamp

    # respiratoryrate = random.randint(10, 30)
    # http_post += "\nvital,location=%s respiratoryrate=" %(mac)
    # http_post += str(respiratoryrate) + " " + timestamp

    http_post += "\'"
    print(http_post)
    subprocess.call(http_post, shell=True)

    time.sleep(1)


