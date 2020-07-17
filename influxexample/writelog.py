#!/usr/bin/python3
import time
import math
import datetime
import subprocess
import sys

#if len(sys.argv) <= 4:
#        print('Example: ./writedata.py 3.136.84.223:8086 testdb test sensorweb')
#        print('open browser with user/password:guest/sensorweb_guest to see waveform at grafana:http://18.217.218.55:3000/d/Yvx-ULCWz/csee4240?orgId=1&refresh=5s')
#        sys.exit()

import logging

logger = logging.getLogger('writelog')
hdlr = logging.FileHandler('./writelog.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)

f_sampling = 10
f_wave = 1
timestamp = datetime.datetime.now().timestamp()

logger.info("Start now ...")
while True:
    # IP:port, databaseName, user, password
    http_post = "curl -i -XPOST \'http://localhost/write?db=testdb\' -u test:sensorweb --data-binary \'"
    for i in range(f_sampling):
        timestamp += 1 / f_sampling
        value = math.sin(2 * math.pi * f_wave * timestamp)
        http_post += "\ntemperature,location=UGA value=" 
        http_post += str(value) + " " + str(int(timestamp*10e8))
        time.sleep(1 / f_sampling)
    http_post += "\'"
    logger.info(http_post)
#    logger.error("test")

