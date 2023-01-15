#!/usr/bin/env python3
import socket as s
import time
#import urllib3
import sys, os
#sys.path.insert(0, os.path.abspath('..'))
import subprocess

#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def start(server):
   ##### Global veriables #########
   c_port = 7777								# Port to bind to
   c_host = "127.0.0.1"

   unit = "airpad"

   url = "https://sensorweb.us:8086"
   db = "testdb"
   user = "test"
   passw = "sensorweb"

   HP = c_host + ":" + str(c_port)
   print("  Opening UDP client socket on (HOST:PORT)", HP)

   sock = s.socket(s.AF_INET, s.SOCK_DGRAM)
   sock.bind((c_host, c_port))

#   a,b,c,d = c_host.split(".")
#   addr_data  = "\'address,location={0} ip1={1},ip2={2},ip3={3},ip4={4}\'" \
#                     .format(unit, str(a), str(b), str(c), str(d))

#   http_post  = "curl -s POST \'http://"+ url+"/write?db="+db+"\' -u "+ user+":"+ passw+" --data-binary " + addr_data
#   print(http_post)
 #  subprocess.call(http_post, shell=True)

#   http_post  = "curl -s --insecure POST \'http://"+ rip+":8086/write?db="+db+"\' -u "+ ruser+":"+ rpassw+" --data-binary " + addr_data
#   print(http_post)
#   subprocess.call(http_post, shell=True)

   pkt_rate = 4  # 4 pkt per second
   num_pkt = 0

   message = "hello"
   print("sending", message)

   byte_message = bytes(message, "utf-8")
# input("-> ")
   sock.sendto(byte_message, server)
   print("sent\n")

   while True:		# loop forever
      data = sock.recv(1024)	# wait to receive data

      num_pkt += 1
   #   multiple dataset with same timestamp
   #   t0 = time.monotonic()
      print("received:", data)
      data = data.rstrip(b'}').split(b',')
      data.pop(0)
      timeIni = int(float(data.pop(0))*1000) * 1000000
      print("processed:", data)

      http_post  = "curl -s -POST \'"+ url+"/write?db="+db+"\' -u "+ user+":"+ passw+" --data-binary \' "
#      http_post2 = "curl -s --insecure -POST \'http://"+rip+":8086/write?db="+db+"\' -u "+ruser+":"+rpassw+" --data-binary \' "

      for f in data:
         http_post  += "\nZ,location=airpad value={1} {2}".format(unit, int(f), timeIni)

#         if(saveRemoteRaw=='true'):
#             http_post2 += "\nZ,location={0} value={1} {2}".format(unit,int(f), timeIni)

         timeIni = timeIni + 10000000 # ??sampling rate is 1000Hz, not 100Hz as pi shake

      http_post += "\'  &"
#      http_post2 += "\'  &"

      print(http_post)

      subprocess.call(http_post, shell=True)
      print("View grafana at https://sensorweb.us:3000/d/hFqA1oGGk/airpad-test?orgId=1&from=now-5m&to=now&refresh=5s")

#      if(saveRemoteRaw=='true'):
#          subprocess.call(http_post2, shell=True)

   #   t1 = time.monotonic()
   #   print("t1-t0= " +str(t1-t0))
   sock.close()

if __name__ == '__main__':
    server = ('127.0.0.1', 8888)
    start(server)
#    start(sys.argv[1], sys.argv[2])