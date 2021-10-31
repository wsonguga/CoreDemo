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


#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def sendData(timestamp, data, channel, fs):
   ##### Global veriables #########
   unit = "be:lt:00.00:00:00"
   url = "https://sensorweb.us:8086"
   db = "algtest"
   user = "test"
   passw = "sensorweb"
   verbose = False

   http_post  = "curl -s -POST \'"+ url+"/write?db="+db+"\' -u "+ user+":"+ passw+" --data-binary \' "
   for value in data:
      http_post += "\n" + "beltsensor" +",location=" + unit + " "
      http_post += channel + "=" + str(value) + " " + str(int(timestamp*10e8))
      timestamp +=  1/fs # ??sampling rate is 1000Hz, not 100Hz as pi shake
   http_post += "\'  &"
   if (verbose):   
      print(http_post)
   subprocess.call(http_post, shell=True)

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
   #  if len(sys.argv) <= 4:
   #      print("Example: " + sys.argv[0] + " https://sensorweb.us:8086 testdb test sensorweb")
   #      print('open browser with user/password:guest/sensorweb_guest to \
   #          see waveform at grafana: https://sensorweb.us:3000/d/Yvx-ULCWz/simsensor?orgId=1&refresh=5s')
   #      sys.exit()
   # ports = list(serial.tools.list_ports.comports())
   # port = None
   # for p in ports:
   #    print(p)
   #    port = p.device

   port = "/dev/ttyUSB0"
   print("Read:", port)
   ser = serial.Serial(port, baudrate=115200, timeout=5)
   print('open browser with user/password:guest/sensorweb_guest to see waveform at grafana: https://www.sensorweb.us:3000/d/pfkrgwTGk/beltsensor?orgId=1&from=now-1m&to=now&refresh=3s')
   fs = 200

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
         timestamp = datetime.datetime.now().timestamp() - (each/fs)
         detail_heart_rate_list, detail_snore_rate_list, detail_respiration_rate_list = parse(receive)
         # sendData(timestamp, detail_heart_rate_list, "HR", fs)
         sendData(timestamp, detail_snore_rate_list, "RR", fs)
         # sendData(timestamp, detail_respiration_rate_list, "SR", fs)
         print(timestamp, " count:" + str(count) + " each:" + str(each) + " verify each:" + str(len(detail_heart_rate_list)))
      else:
         subprocess.call("./usbWrite.py", shell=True)

      time.sleep(1)

#    start(sys.argv[1], sys.argv[2])
