#!/usr/bin/env python3
import socket as s
import time
#import urllib3
import sys, os
#sys.path.insert(0, os.path.abspath('..'))
import subprocess
# import random
# import numpy as np
import datetime
import serial
import serial.tools.list_ports

from util import local_time_epoch
from util import write_influx

# def read_next(fs):
#     data1 = np.random.randint(10, 20, size=fs)
#     data2 = np.random.randint(20, 30, size=fs)
#     data3 = np.random.randint(30, 40, size=fs)
#     time.sleep(1) # sleep one second
#     return data1, data2, data3

def parse(data):
   length = len(data)
   detail_heart_rate_list = []
   detail_snore_rate_list = []
   detail_respiration_rate_list = []
   if length % 16 == 0:
      package_number = int(length / 16)
      for i in range(0, package_number):
          start = 0 + i * 16
          end = (1 + i) * 16
          data_array = data[start:end]
          #print('data_array', data_array)
          header = data_array[0]
          type = data_array[1]
          number = data_array[3] * 256 + data_array[2]
          heart_rate = data_array[5] * 256 + data_array[4]
          snore_rate = data_array[7] * 256 + data_array[6]
          respiration_rate = data_array[9] * 256 + data_array[8]
          heart_rate2 = data_array[11] * 256 + data_array[10]
          snore_rate2 = data_array[13] * 256 + data_array[12]
          respiration_rate2 = data_array[15] * 256 + data_array[14]

          #print(heart_rate, snore_rate, respiration_rate,heart_rate2, snore_rate2, respiration_rate2)
          detail_heart_rate_list.append(heart_rate)
          detail_snore_rate_list.append(snore_rate)
          detail_respiration_rate_list.append(respiration_rate)
          detail_heart_rate_list.append(heart_rate2)
          detail_snore_rate_list.append(snore_rate2)
          detail_respiration_rate_list.append(respiration_rate2)
      # print(detail_respiration_rate_list)
   return detail_heart_rate_list, detail_snore_rate_list, detail_respiration_rate_list

if __name__ == '__main__':

   port = "/dev/ttyUSB0"
   print("Read:", port)
   ser = serial.Serial(port, baudrate=115200, timeout=5)
   print('open browser with user/password:guest/sensorweb_guest to see waveform at grafana: https://www.sensorweb.us:3000/d/pfkrgwTGk/beltsensor?orgId=1&from=now-1m&to=now&refresh=3s')
   fs = 200

   dest = {'ip':'https://sensorweb.us', 'db':'testdb', 'user':'test', 'passw':'sensorweb'}

#   subprocess.call("/opt/belt/beltWrite.py", shell=True)
   while(True):
      count = ser.inWaiting()
      print('inWaiting:', count)
      # for c in ser.read():
      #    print('result ---------', c)
      if count > 0:
         receive = ser.read(ser.inWaiting())
     #    print(time.time(), "-- receive --", receive)
         # data1, data2, data3 = read_next(fs)
         count = len(receive)
         each = float(count)/8
         start_timestamp = datetime.datetime.now().timestamp() - (each/fs)
         detail_heart_rate_list, detail_snore_rate_list, detail_respiration_rate_list = parse(receive)
         write_influx(dest, "unit.name", "beltsensor", "HR", detail_heart_rate_list, start_timestamp, fs)
         write_influx(dest, "unit.name", "beltsensor", "RR", detail_respiration_rate_list, start_timestamp, fs)
         write_influx(dest, "unit.name", "beltsensor", "SR", detail_snore_rate_list, start_timestamp, fs)

         print(start_timestamp, " count:" + str(count) + " each:" + str(each) + " verify each:" + str(len(detail_heart_rate_list)))
      # else: # some serial ports require a write operation to start sending data out, then uncomment below
      #    subprocess.call("/opt/belt/beltWrite.py", shell=True)

      time.sleep(1)
