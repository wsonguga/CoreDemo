from influxdb import InfluxDBClient
from influx import InfluxDB
import numpy as np
import itertools 
import math
import datetime
import subprocess
import sys
import operator
from datetime import datetime 
from datetime import timezone
import types

#Remote data base information
IP = 'localhost'
PORT = 8086
USER = 'sili'
PASSWORD = 'sensorweb'
DBNAME = 'floorseis'


#Local database information
Local_Database_name = 'test2'

#Time range
starttime = datetime(2020, 6, 4,15,40,0)
endtime = datetime(2020, 8, 4,15,41,0)




#starttime = "2020-06-04T15:40:00.000000000Z"
#endtime = "2020-06-04T15:42:00.000000000Z"


#utc_time = starttime.replace(tzinfo = timezone.utc)
timestamp = starttime.timestamp()*1000
start_str = str(int((timestamp)*1000000))

#utc_time = endtime.replace(tzinfo = timezone.utc)
timestamp = endtime.timestamp()*1000
end_str=str(int((timestamp)*1000000))

print(start_str,end_str)


client = InfluxDBClient(IP, PORT, USER, PASSWORD, DBNAME)
client2 = InfluxDB('http://127.0.0.1:8086')

#get series

query = 'show series'
result = client.query(query)

points = list(result.get_points())
#value =  np.append(value,np.array(list(map(operator.itemgetter('value'), points))))
print(points[0]['key'])
print(points)

def copy_all_points(sname):
    sname='test'
    query = 'SELECT * FROM '+ sname +' WHERE time > '+start_str+' and time < '+end_str
    result = client.query(query)
    values = list(result.get_points())
    print(values[0])

    for point in values:
        tag={}
        field={}
        for key, v in point.items():
            if key=='time':
                point_time = datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%fZ')
            elif type(v) == type('a'):
                tag[key]=v
            else:
                field[key]=v
        #print(tag,field,point_time)
        client2.write(Local_Database_name, sname, fields=field,tags=tag,time=point_time)





#get and upload values


for i in range(len(points)):
    read = points[i]['key']
    sname = read.split(',')[0] 
    query = 'SELECT * FROM '+ sname +' WHERE time > '+start_str+' and time < '+end_str
    result = client.query(query)
    values = list(result.get_points())
    print(values[0])

    for point in values:
        tag={}
        field={}
        for key, v in point.items():
            if key=='time':
                if len(v)<21:
                    point_time = datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ')
                else:
                    point_time = datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%fZ')
            elif type(v) == type('a'):
                tag[key]=v
            else:
                field[key]=v
        #print(tag,field,point_time)
        client2.write(Local_Database_name, sname, fields=field,tags=tag,time=point_time)

