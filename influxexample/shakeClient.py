#!/usr/bin/env python3
import socket as s
import subprocess

with open('/opt/settings/sys/ip.txt', 'r') as file:
    host = file.read().strip()

unit = "airpad"

url = "https://sensorweb.us:8086"
db = "testdb"
user = "test"
passw = "sensorweb"

port = 8888                             # Port to bind to
sock = s.socket(s.AF_INET, s.SOCK_DGRAM | s.SO_REUSEADDR)
sock.bind((host, port))
print "Waiting for data on Port:", port
while 1:                                # loop forever
   data, addr = sock.recvfrom(1024)    # wait to receive data
   print data

   data = data.rstrip(b'}').split(b',')
   data.pop(0)
   timeIni = int(float(data.pop(0))*1000) * 1000000
   print("processed:", data)

   http_post  = "curl -s -POST \'"+ url+"/write?db="+db+"\' -u "+ user+":"+ passw+" --data-binary \' "

   for f in data:
      http_post  += "\nZ,location=airpad value={1} {2}".format(unit, int(f), timeIni)
      timeIni = timeIni + 10000000 # ??sampling rate is 1000Hz, not 100Hz as pi shake

   http_post += "\'  &"

   print(http_post)

   subprocess.call(http_post, shell=True)
   print("View grafana at https://sensorweb.us:3000/d/hFqA1oGGk/airpad-test?orgId=1&from=now-5m&to=now&refresh=5s")

