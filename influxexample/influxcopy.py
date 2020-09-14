#!/usr/bin/env python3
# Migrate the data from one Influxdb database to another.
# add argument '-h' for help

# Usage:

# influxcopy.py sURL sDB dURL dDB startTime endTime
# positional arguments:

# sURL the URL of source database.
# sDB name of the source database.
# dURL the URL of destination database.
# dDB name of the destination database.
# startTime start time. format: Year-Mon-Day-Hour-Min-Sec
# endTime end time. format: Year-Mon-Day-Hour-Min-Sec


import argparse
from influxdb import InfluxDBClient
import numpy as np
import time
import math
import datetime
import sys
from datetime import datetime 


def get_arguments():
    parser = argparse.ArgumentParser(description='Migrate data from one influxDB database to another.')
    parser.add_argument('sURL',
                        type=str,
                        help='the URL of source database.')
    parser.add_argument('sDB',
                        type=str,
                        help='name of the source database.')
    parser.add_argument('dURL',
                        type=str,
                        help='the URL of destination database.')
    parser.add_argument('dDB',
                        type=str,
                        help='name of the destination database.')
    parser.add_argument('startTime',
                        type=str,
                        help='start time. format: Year-Mon-Day-Hour-Min-Sec')
    parser.add_argument('endTime',
                        type=str,
                        help='end time. format: Year-Mon-Day-Hour-Min-Sec')
    
    return parser.parse_args()


def datetime_convert(startDate, endDate):
    year, mon, day, hour, min, sec = startDate.split('-')
    sDate = datetime(int(year), int(mon), int(day), int(hour), int(min), int(sec))

    year, mon, day, hour, min, sec = endDate.split('-')
    eDate = datetime(int(year), int(mon), int(day), int(hour), int(min), int(sec))

    return sDate, eDate


def data_migration(startTime, endTime, args):
    
    timestamp = startTime.timestamp()*1000
    start_str = str(int((timestamp)*1000000))

    timestamp = endTime.timestamp()*1000
    end_str=str(int((timestamp)*1000000))

    result = sClient.query('show series')
    points = list(result.get_points())

    for i in range(len(points)):
        read = points[i]['key']
        sname = read.split(',')[0]
        copyQuery = 'SELECT * FROM ' + sname + ' WHERE time > ' + start_str + ' and time < ' + end_str
        result = sClient.query(copyQuery)
        values = list(result.get_points())

        data = []
        for point in values:
            tag = {}
            field = {}
            for key, value in point.items():
                if key == 'time':
                    if len(value) < 21:
                        point_time = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
                    else:
                        point_time = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')
                elif type(value) == type('a'):
                    tag[key] = value
                else:
                    field[key] = value

                data.append(
                    {
                        "measurement": sname,
                        "tags" : tag,
                        "fields" : field,
                        "time": point_time
                    }
                )
        dClient.write_points(data, database = args.dDB, time_precision = 'ms', batch_size = write_batch_size, protocol = 'json')
    return None
    

def main():
    sTime, eTime = datetime_convert(args.startTime, args.endTime)
    leftWindow = sTime

    client_write_start_time = time.perf_counter()
    while True:
        if (eTime - leftWindow).seconds > 5 * 60:
            rightWindow = leftWindow + datetime.timedelta(minutes=5)
        else:
            rightWindow = eTime

        data_migration(leftWindow, rightWindow, args)
        if (eTime - leftWindow).seconds < 5 * 60:
            break
        leftWindow = rightWindow
    
    client_write_end_time = time.perf_counter()
    print("Migration completed! Data write time: {time}s".format(time = client_write_end_time - client_write_start_time))
    return None



if __name__ == "__main__":
    args = get_arguments()
    # The ideal batch size for InfluxDB is 5,000-10,000 points.
    write_batch_size = 5000
    sClient = InfluxDBClient(host=args.sURL, 
                            port=8086, 
                            username='root', 
                            password='root', 
                            database=args.sDB)
    
    dClient = InfluxDBClient(host=args.dURL, 
                            port=8086, 
                            username='root', 
                            password='root', 
                            database=args.dDB,
                            ssl=True)
    main()
