#!/usr/bin/env python3

import time
import math
import subprocess
import sys
import random
import webbrowser
import numpy as np
from datetime import datetime
from dateutil import tz
import pytz
from influxdb import InfluxDBClient
import operator

# python API client for influx 2.x
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS



# This function converts the time string to epoch time xxx.xxx (second.ms).
# Example: time = "2020-08-13T02:03:00.200", zone = "UTC" or "America/New_York"
# If time = "2020-08-13T02:03:00.200Z" in UTC time, then call timestamp = local_time_epoch(time[:-1], "UTC"), which removes 'Z' in the string end
def local_time_epoch(time, zone):
    local_tz = pytz.timezone(zone)
    try:
        localTime = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%f")
    except:
        localTime = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
    local_dt = local_tz.localize(localTime, is_dst=None)
    # utc_dt = local_dt.astimezone(pytz.utc)
    epoch = local_dt.timestamp()
    # print("epoch time:", epoch) # this is the epoch time in seconds, times 1000 will become epoch time in milliseconds
    # print(type(epoch)) # float
    return epoch

def influx_query_time_epoch(time, zone):
    local_tz = pytz.timezone(zone)
    try:
        localTime = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
    except:
        localTime = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
        
    local_dt = local_tz.localize(localTime, is_dst=None)
    # utc_dt = local_dt.astimezone(pytz.utc)
    epoch = local_dt.timestamp()
    # print("epoch time:", epoch) # this is the epoch time in seconds, times 1000 will become epoch time in milliseconds
    # print(type(epoch)) # float
    return epoch


# This function converts the epoch time xxx.xxx (second.ms) to time string.
# Example: time = "2020-08-13T02:03:00.200", zone = "UTC" or "America/New_York"
# If time = "2020-08-13T02:03:00.200Z" in UTC time, then call timestamp = local_time_epoch(time[:-1], "UTC"), which removes 'Z' in the string end
def epoch_time_local(epoch, zone):
    local_tz = pytz.timezone(zone)
    time = datetime.fromtimestamp(epoch).astimezone(local_tz).strftime("%Y-%m-%dT%H:%M:%S.%f")
    return time 

# This function converts the grafana URL time to epoch time. For exmaple, given below URL
# https://sensorweb.us:3000/grafana/d/OSjxFKvGk/caretaker-vital-signs?orgId=1&var-mac=b8:27:eb:6c:6e:22&from=1612293741993&to=1612294445244
# 1612293741993 means epoch time 1612293741.993; 1612294445244 means epoch time 1612294445.244
def grafana_time_epoch(time):
    return time/1000

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
    prefix_post  = "curl -i -k -XPOST \'"+ influx['ip']+":8086/write?db="+influx['db']+"\' -u "+ influx['user']+":"+ influx['passw']+" --data-binary \' "
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

# This function read an array of data from influxdb.
# influx - the InfluxDB info including ip, db, user, pass. Example influx = {'ip': 'https://sensorweb.us', 'db': 'testdb', 'user':'test', 'passw':'sensorweb'}
# dataname - the dataname such as temperature, heartrate, etc
# start_timestamp, end_timestamp - the epoch time (in second) of the first element in the data array, such as datetime.now().timestamp()
# unit - the unit location name tag
def read_influx(influx, unit, table_name, data_name, start_timestamp, end_timestamp, condition="location"):
    client = InfluxDBClient(influx['ip'].split('//')[1], '8086', influx['user'], influx['passw'], influx['db'],  ssl=True)
    query = 'SELECT "' + data_name + '" FROM "' + table_name + f'" WHERE "{condition}" = \''+unit+'\' AND time >= '+ str(int(start_timestamp*10e8))+' AND time <= '+str(int(end_timestamp*10e8))
    # query = 'SELECT last("H") FROM "labelled" WHERE ("location" = \''+unit+'\')'

    # print(query)
    result = client.query(query)
    # print(result)

    points = list(result.get_points())
    values =  list(map(operator.itemgetter(data_name), points))
    times  =  list(map(operator.itemgetter('time'),  points))
    # print(times)
    # times = [local_time_epoch(item[:-1], "UTC") for item in times] # convert string time to epoch time
    # print(times)

    data = values #np.array(values)
    # print(data, times)
    return data, times

def read_influx2(influx, unit, table_name, data_name, start_timestamp, end_timestamp, condition="location"):
    """This function shows an example how to read data points from influx 2.x database
    """
    bucket = influx['bucket']
    org = influx['org']
    token = influx['token']
    url = influx['ip'] + ":8086"
    start = str(datetime.fromtimestamp(start_timestamp).isoformat()) + 'Z'
    end = str(datetime.fromtimestamp(end_timestamp).isoformat()) + 'Z'

    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )
    
    query_api = client.query_api()
    query = f' from(bucket:"{bucket}")\
    |> range(start: {start}, stop: {end})\
    |> filter(fn:(r) => r._measurement == "{table_name}")\
    |> filter(fn: (r) => r[{condition}] == "{unit}")\
    |> filter(fn:(r) => r._field == "{data_name}" )'
    result = query_api.query(org=org, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_field(), record.get_value()))
            
    return results

def write_influx2(influx, unit, table_name, data_name, data, start_timestamp, fs):
    """This function shows an example how to write a point into the influx 2.x database
    """
    # influx, unit, table_name, data_name, data, start_timestamp, fs
    timestamp = start_timestamp
    bucket = influx['bucket']
    org = influx['org']
    token = influx['token']
    url = influx['ip'] + ":8086"
    start = str(int(start_timestamp*10e8))


    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )
    write_api = client.write_api(write_options=SYNCHRONOUS)

    max_size = 100
    total = len(data)
    count = 0
    
    for value in data:
        count += 1
        if count >= max_size:
            print("Write to influx: ", table_name, data_name, count)
            p = influxdb_client.Point(table_name).tag("location", unit).field(data_name, value).time(start)
            write_api.write(bucket=bucket, org=org, record=p)
            total = total - count
            count = 0
        start += 1 / fs
