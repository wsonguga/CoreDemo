#!/usr/bin/env python3
#!sudo apt-get install python3-pip
import socket as s
import time
#import urllib3
import sys, os
#sys.path.insert(0, os.path.abspath('..'))
import subprocess
# import random
# import numpy as np
import datetime
#!pip3 install pyserial
import serial
import serial.tools.list_ports
#!pip3 install netifaces
import netifaces

def mac_address():
   macEth = "unit.name"
   data = netifaces.interfaces()
   for i in data:
      if i == 'eth0': #'en0': # 'eth0':
         interface = netifaces.ifaddresses(i)
         info = interface[netifaces.AF_LINK]
         if info:
            macEth = interface[netifaces.AF_LINK][0]["addr"]
   return macEth

def parse(data):
   length = len(data)
   print(" ".join(hex(n) for n in data))  

   # this line below shall be modified based on your actual data structure
   # each element in result shalll be one sensor reading
   result = data 
   # size = len(result)
   return result

# This function write an array of data to influxdb. It assumes the sample interval is 1/fs.
# influx - the InfluxDB info including ip, db, user, pass. Example influx = {'ip': 'https://sensorweb.us', 'db': 'algtest', 'user':'test', 'passw':'sensorweb'}
# dataname - the dataname such as temperature, heartrate, etc
# timestamp - the epoch time (in second) of the first element in the data array, such as datetime.now().timestamp()
# fs - the sampling frequency of readings in data
# unit - the unit location name tag
def write_influx(influx, unit, table_name, data_name, data, start_timestamp, fs):
    # print("epoch time:", timestamp) 
    timestamp = start_timestamp
    max_size = 100
    count = 0
    total = len(data)
    prefix_post  = "curl -s -POST \'"+ influx['ip']+":8086/write?db="+influx['db']+"\' -u "+ influx['user']+":"+ influx['passw']+" --data-binary \' "
    http_post = prefix_post
    for value in data:
        count += 1
        http_post += "\n" + table_name +",location=" + unit + " "
        http_post += data_name + "=" + str(value) + " " + str(int(timestamp*10e8))
        timestamp +=  1/fs
        if(count >= max_size):
            http_post += "\'  &"
            # print(http_post)
            print("Write to influx: ", table_name, data_name, count)
            subprocess.call(http_post, shell=True)
            total = total - count
            count = 0
            http_post = prefix_post
    if count != 0:
        http_post += "\'  &"
        # print(http_post)
        print("Write to influx: ", table_name, data_name, count, data)
        subprocess.call(http_post, shell=True)

if __name__ == '__main__':

   if(len(sys.argv) > 1):
      port = sys.argv[1]
   else:
      port = "/dev/ttyUSB0" # default
      print(f"Usage: python3 {sys.argv[0]} port")
      print(f"\t Examples: \n\t\tpython3 {sys.argv[0]} /dev/ttyUSB0 (read from USB-serial) \n\t\tpython3 {sys.argv[0]} /dev/ttyS0 (for UART-serial) \n\t\tpython3 {sys.argv[0]} none (for simulation mode)\n")
      exit()

   print("Read:", port)
   ser = 0
   if port != "none":
      ser = serial.Serial(port, baudrate=115200, timeout=5)
      has_serial = True
      macEth = mac_address()
   else:
      has_serial = False
      macEth = 'unit.name'
   fs = 100
   print("My ethernet MAC is: ", macEth)
   print(f'open browser with user/password:guest/sensorweb_guest to see waveform at grafana: \n\thttps://www.sensorweb.us:3000/d/VgfUaF3Gz/bdotv2-plot?orgId=1&var-mac1={macEth}&from=now-1m&to=now&refresh=5s')


   dest = {'ip':'https://sensorweb.us', 'db':'shake', 'user':'test', 'passw':'sensorweb'}

   # some serial ports require a write operation to start sending data out, then uncomment below and replace with a serial write program
#   subprocess.call("/opt/belt/beltWrite.py", shell=True)
   start_timestamp = datetime.datetime.now().timestamp()
   while(True):
      time.sleep(1)
      if has_serial:
         count = ser.inWaiting()
      else:
         count = fs # 
      print('inWaiting:', count)
      if count > 0:
         if has_serial:
            receive = ser.read(ser.inWaiting())
         else:
            receive = [10, 20, 30, 40, 50]*int(fs/5) # np.random.randint(10, 200, size=fs)  #  
         end_timestamp = datetime.datetime.now().timestamp()      
         # print(f'serial ({len(receive)}): {receive}')

         # start_timestamp = datetime.datetime.now().timestamp() - (each/fs)
         data = parse(receive)
         ### !!! notice that fd is not fs and may be non-integer considering serial port uncertain delays
         fd = (len(data))/(end_timestamp - start_timestamp) 
         write_influx(dest, macEth, "Z", "value", data, start_timestamp, fd)

         print(f'start: {start_timestamp}, end: {end_timestamp}, size:{len(data)}, fd:{fd}')
      # some serial ports require a write operation to start sending data out, then uncomment below and replace with a serial write program
      # else: 
      #    subprocess.call("/opt/belt/beltWrite.py", shell=True)
      start_timestamp = end_timestamp
