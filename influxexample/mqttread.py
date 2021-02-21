#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import time
from util import write_influx
from datetime import datetime


dest = {'ip':'https://sensorweb.us', 'db':'testdb', 'user':'test', 'passw':'sensorweb'}
# Visit URL: https://sensorweb.us:3000/d/KeEHZfJMz/shelly-sensors?orgId=1&from=now-5m&to=now (guest/sensorweb_guest)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))  
    client.subscribe("shellies/shellyem3-D8BFC01A80A4/emeter/0/power")  
    # client.subscribe("test")   
 
def on_message(client, userdata, msg):
    print(msg.topic, float(msg.payload))
    print(msg.payload)

    start_timestamp = datetime.now().timestamp()
    fs = 1
    write_influx(dest, "shelly.ht.000000", "shellysensor", "HT", [float(msg.payload)], start_timestamp, fs)
 
client_id = "dots"# time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))   
client = mqtt.Client(client_id)    
client.username_pw_set("sili", "sensorweb") 
client.on_connect = on_connect
client.on_message = on_message
client.connect("sensorweb.us", 1883, 60)   #
# client.connect("sensorweb.us", 1883, 60)   #
client.loop_forever()
