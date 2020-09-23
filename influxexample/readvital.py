#!/usr/bin/env python3

import numpy as np
import csv
import matplotlib.pyplot as plt
from influxdb import InfluxDBClient
import operator

ip = "sensorweb.us" 
unit = "b8:27:eb:97:f5:ac"
# floordot: b8:27:eb:63:da:62

client = InfluxDBClient(ip, "8086", "test", "sensorweb", "healthresult",  ssl=True)

# get heart rate
query = 'SELECT last("hr") FROM "hrate" WHERE ("location" = \''+unit+'\')'
result = client.query(query)
points = list(result.get_points())
values =  map(operator.itemgetter('last'), points)
times  =  map(operator.itemgetter('time'),  points)
data = np.array(list(values))
print("heart rate: " + str(data[0]))

# get respiratory rate
query = 'SELECT last("rr") FROM "rrate" WHERE ("location" = \''+unit+'\')'
result = client.query(query)
points = list(result.get_points())
values =  map(operator.itemgetter('last'), points)
times  =  map(operator.itemgetter('time'),  points)
data = np.array(list(values))
print("respiratory rate: " + str(data[0]))

# get in/out bed status
query = 'SELECT last("bs") FROM "bedStatus" WHERE ("location" = \''+unit+'\')'
result = client.query(query)
points = list(result.get_points())
values =  map(operator.itemgetter('last'), points)
times  =  map(operator.itemgetter('time'),  points)
data = np.array(list(values))
# 1 - in bed; 0 - out bed; others - no meaning
print("in/out bed: " + str(data[0]))

# get raw data
stampIni = "2020-08-13T14:10:00.000Z" # UTC time = EST time + 4
stampEnd = "2020-08-13T14:10:07.000Z"
client = InfluxDBClient(ip, "8086", "test", "sensorweb", "shake",  ssl=True)
query = 'SELECT "value" FROM Z WHERE ("location" = \''+unit+'\')  and time >= \''+stampIni+'\' and time <= \''+stampEnd+'\'   '
result = client.query(query)
points = list(result.get_points())
values =  map(operator.itemgetter('value'), points)
times  =  map(operator.itemgetter('time'),  points)
data = np.array(list(values))
fs = 100 # for vibration data
if(len(data) == 0):
  print("No data in the chosen time range!")
  quit()
plt.figure(figsize=(20, 4))
plt.title("vital signs induced vibrations")
plt.plot(data)
plt.show()