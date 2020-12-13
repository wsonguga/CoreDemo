#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import time
 
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))  
    client.subscribe("shellies/shellyem3-D8BFC01A80A4/emeter/0/power")  
 
 
def on_message(client, userdata, msg):
    print(msg.topic+" " + ":" + str(msg.payload))  
 
 
client_id = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))   
client_id
client = mqtt.Client(client_id)    
client.username_pw_set("sili", "sensorweb") 
client.on_connect = on_connect
client.on_message = on_message
client.connect("test.mosquitto.org", 1883, 60)   #
client.loop_forever()