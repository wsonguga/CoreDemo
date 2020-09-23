#!/usr/bin/env python3
# Migrate the data from one Influxdb database to another.
# add argument '-h' for help

import argparse
from influxdb import InfluxDBClient
import numpy as np
import time
import math
import datetime
import sys
import urllib3
# from datetime import datetime
urllib3.disable_warnings()


def get_arguments():
    parser = argparse.ArgumentParser(description="""Migrate data from one influxDB database to another.""")

    parser.add_argument('measurement',
                        type=str,
                        help='name of the measurement, type ALL for all.')
    parser.add_argument('sURL',
                        type=str,
                        help='the URL of source database. http://example.com')
    parser.add_argument('sDB',
                        type=str,
                        help='name of the destination database. http://example.com')
    parser.add_argument('sUser',
                        type=str,
                        help='username of the source database.')
    parser.add_argument('sPasswd',
                        type=str,
                        help='password of the source database.')
    parser.add_argument('dURL',
                        type=str,
                        help='the URL of destination database.')
    parser.add_argument('dDB',
                        type=str,
                        help='name of the destination database.')
    parser.add_argument('dUser',
                        type=str,
                        help='username of the destination database.')
    parser.add_argument('dPasswd',
                        type=str,
                        help='password of the destination database.')
    parser.add_argument('startTime',
                        type=str,
                        help='start time. format: Year-Mon-DayTHour:Min:Sec')
    parser.add_argument('endTime',
                        type=str,
                        help='end time. format: Year-Mon-DayTHour:Min:Sec')
    
    return parser.parse_args()


def datetime_convert(startDate, endDate):
    leftT, rightT = startDate.split('T')
    year, mon, day = leftT.split('-')
    hour, min, sec = rightT.split(':')
    sDate = datetime.datetime(int(year), int(mon), int(day), int(hour), int(min), int(sec))

    leftT, rightT = endDate.split('T')
    year, mon, day = leftT.split('-')
    hour, min, sec = rightT.split(':')
    eDate = datetime.datetime(int(year), int(mon), int(day), int(hour), int(min), int(sec))

    return sDate, eDate


def data_migration(startTime, endTime, args):
    # If a certain measurement is specified or not
    if args.measurement != 'ALL':
        isAll = False
    else:
        isAll = True

    start_timestamp = startTime.timestamp()*1000
    start_str = str(int((start_timestamp)*1000000))

    end_timestamp = endTime.timestamp()*1000
    end_str=str(int((end_timestamp)*1000000))

    result = sClient.query('show series')
    points = list(result.get_points())

    print("\Points:", points)

    for i in range(len(points)):
        read = points[i]['key']
        print("\nRead:", read)
        if isAll == False:
            sname = args.measurement
        else:
            sname = read.split(',')[0]
        
        if sname != read.split(',')[0]:
            continue
        
        copyQuery = 'SELECT * FROM ' + sname + ' WHERE time > ' + start_str + ' and time < ' + end_str
        print("\nQueries:", copyQuery)
        result = sClient.query(copyQuery)
        values = list(result.get_points())
        print("\nValues:", values)

        data = []
        for point in values:
            tag = {}
            field = {}
            for key, value in point.items():
                if key == 'time':
                    if len(value) < 21:
                        point_time = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
                    else:
                        point_time = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')
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

    sTime = sTime.timestamp() * 1000
    eTime = eTime.timestamp() * 1000
    print("\nMigration completed! Data write time: {time}s".format(time = client_write_end_time - client_write_start_time))
    print("Click here to see the results in Grafana:\n" +
            "https://sensorweb.us:3000/d/L3IBhqdGz/migration-example?orgId=1&from=" +
            str(int(sTime)) + "&to=" + str(int(eTime)))
    return None



if __name__ == "__main__":
    # arguments examination
    if len(sys.argv) <= 10:
        print("Usage: \n" + sys.argv[0] + " sname sIP sDB sUser sPass dIP dDB dUser dPass startTime endTime")
        print("Example (copy all): \n" + sys.argv[0] + " ALL https://sensorweb.us shake test sensorweb https://sensorweb.us testdb test sensorweb 2020-08-07T19:22:31 2020-08-07T19:22:35")
        print("Example (copy series Z only): \n" + sys.argv[0] + " Z https://sensorweb.us shake test sensorweb https://sensorweb.us testdb test sensorweb 2020-08-07T19:22:31 2020-08-07T19:22:35")
        # print("\nOpen browser with user/password:guest/sensorweb_guest to see waveform at grafana:\n \
        #         https://grafana.sensorweb.us/d/L3IBhqdGz/migration-example?orgId=1&from=1596842552000&to=1596842555002")
        sys.exit()
        
    args = get_arguments()
    # The ideal batch size for InfluxDB is 5,000-10,000 points.
    write_batch_size = 1000

    if 'https' in args.sURL:
        isSSL = True
    else:
        isSSL = False
    args.sURL = args.sURL.split('//')[1]
    
    sClient = InfluxDBClient(host=args.sURL, 
                            port=8086, 
                            username=args.sUser, 
                            password=args.sPasswd, 
                            database=args.sDB,
                            ssl=isSSL)
    
    if 'https' in args.dURL:
        isSSL = True
    else:
        isSSL = False
    args.dURL = args.dURL.split('//')[1]

    dClient = InfluxDBClient(host=args.dURL, 
                            port=8086, 
                            username=args.dUser, 
                            password=args.dPasswd, 
                            database=args.dDB,
                            ssl=isSSL)
    main()