'''
This program is an influxDB local cache program like HTTP. 
When function readData() is called, the new data from the remote DB will be cached in the local DB. Besides giving to the return; If user visits the same time range of data again, this program will automatically read from the local DB. The database, series name and tag/label names will be created locally and automaticallyas needed.
Also, if the local influxdb and grafana installation does not exist, trigger the correct command to install it.
'''

'''logic: firstly read from local. If no data, read from remote and save the data to local. Lastly, return the requested data.
Noted: if no influxdb or grafana installed in local. Prompt users to install.
'''
#!/usr/bin/env python3
import sys, os
from influxdb import InfluxDBClient
import datetime, time
import urllib3
urllib3.disable_warnings()

src_info = {
    "remote_ip" : "https://sensorweb.us",
    "remote_port" : "8086",
    "local_ip" : "http://localhost",
    "local_port" : "8086",
    "remote_username" : "test",
    "remote_passwd" : "sensorweb",
    "local_username" : "qi",
    "local_passwd" : "7781",
    "db" : "waveform",
    "measurement" : "sensor_01",
    "fields" : ["Ib", "Ia"], # fields could be an array
    # "tags" : {"case":['attack_01', 'attack_02', 'attack_03', 
    #                   'attack_04', 'attack_05', 'attack_06', 
    #                   'attack_07', 'attack_08', 'attack_09', 
    #                   'attack_10', 'attack_11', 'attack_12', 
    #                   'attack_13', 'attack_14', 'attack_15', 
    #                   'normal_01', 'normal_02', 'normal_03', 
    #                   'normal_04', 'normal_05', 'normal_06']}
    #                    tags could be an array
    "tag_key" : "case",
    "tag_value" : "attack_01",
    "startUTCTime" : "2020-02-18T19:06:14",
    "endUTCTime" : "2020-02-18T19:06:15",
}

def test_software_installed():
    '''
    This function is to examine if the grafana and influxDB are installed on the machine.
    '''
    influxCmd = 'influx'
    grafanaCmd = 'grafana-cli'
    influxInstalled = False
    grafanaInstalled = False
    for cmdpath in os.environ['PATH'].split(':'):
        if os.path.isdir(cmdpath) and (influxCmd in os.listdir(cmdpath)):
            influxInstalled = True

        if os.path.isdir(cmdpath) and (grafanaCmd in os.listdir(cmdpath)):
            grafanaInstalled = True
    
    if not influxInstalled:
        print("Influxdb not installed, please check this link to install: https://docs.influxdata.com/influxdb/v1.8/introduction/install/")

    if not grafanaInstalled:
        print("grafana not installed, please check this link to install: https://grafana.com/docs/grafana/latest/installation/")
    
    if not (influxInstalled and grafanaInstalled):
        print("program exiting...")
        exit()

    return



def datetime_convert(startDate, endDate):
    '''
    This function is to convert the datetime from UTC to influxDB time format
    '''
    leftT, rightT = startDate.split('T')
    year, mon, day = leftT.split('-')
    hour, min, sec = rightT.split(':')
    sDate = datetime.datetime(int(year), int(mon), int(day), int(hour), int(min), int(sec))

    leftT, rightT = endDate.split('T')
    year, mon, day = leftT.split('-')
    hour, min, sec = rightT.split(':')
    eDate = datetime.datetime(int(year), int(mon), int(day), int(hour), int(min), int(sec))

    return sDate, eDate


def write_date(info=src_info.copy(), write_local=True):
    pass
    return

def write_localDB(dataRead):
    '''
    This function is to write the data to local DB.
    '''
    info = src_info.copy()
    measurement = info["measurement"]
    dbname = info["db"]
    write_batch_size = 1000

    if 'https' in info["local_ip"]:
        isSSL = True
    else:
        isSSL = False
    info["local_ip"] = info["local_ip"].split('//')[1]

    # test the connection with local DB
    try:
        client = InfluxDBClient(host=info["local_ip"],
                                port=info["local_port"], 
                                username=info["local_username"], 
                                password=info["local_passwd"],
                                database=info["db"],
                                ssl=isSSL
                                )
    except Exception as e:
        print("Error: %s" %e)
        exit()

    data = []
    for point in dataRead:
        tag = {}
        field = {}
        for key, value in point.items():
            if key == 'time':
                pointTime = value
            elif type(value) == type('a'):
                tag[key] = value
            else:
                field[key] = value

        data.append(
            {
                "measurement": measurement,
                "tags": tag,
                "fields": field,
                "time" : pointTime,
            }
        )

    client_write_start_time = time.perf_counter()
    try:
        client.write_points(data, database = dbname, time_precision = 'ms', batch_size = write_batch_size, protocol = 'json')
    except Exception as e:
        print("Error: %s" %e)
        exit()
    client_write_end_time = time.perf_counter()
    print("Writing to local DB completed! Data write time: {time}s".format(time=client_write_end_time - client_write_start_time))
    return 
    

    

def read_remoteDB(info=src_info.copy()):
    readSuccess = False

    if 'https' in info["remote_ip"]:
        isSSL = True
    else:
        isSSL = False
    info["remote_ip"] = info["remote_ip"].split('//')[1]
    
    # test the connection with local DB
    try:
        client = InfluxDBClient(host=info["remote_ip"],
                                port=info["remote_port"], 
                                username=info["remote_username"], 
                                password=info["remote_passwd"],
                                database=info["db"],
                                ssl=isSSL
                                )
    except Exception as e:
        print("Error: %s" %e)
        exit()

    field_list = ''
    for i in info["fields"]:
        field_list += i + ','
    field_list = field_list[:-1]

    sTime, eTime = datetime_convert(info["startUTCTime"], info["endUTCTime"])
    sTime_str = str(int((sTime.timestamp()*1000)*1000000))
    eTime_str = str(int((eTime.timestamp()*1000)*1000000))
    
    query = 'SELECT ' + field_list + "::field, " +"case::tag "+ "FROM " + info["measurement"] + ' WHERE time > ' + sTime_str + ' and time < ' + eTime_str

    try:
        result = client.query(query)
    except Exception as e:
        print("Error: %s" %e)
        exit()

    
    data = list(result.get_points())
    readSuccess = True

    write_localDB(data)
    return data, readSuccess

def read_localDB(info=src_info.copy()):
    '''
    This function is to read the data from local DB. If data doesn't exist, then return false.
    '''
    dbExisted = False
    readSuccess = False

    if 'https' in info["local_ip"]:
        isSSL = True
    else:
        isSSL = False
    info["local_ip"] = info["local_ip"].split('//')[1]

    # test the connection with local DB
    try:
        client = InfluxDBClient(host=info["local_ip"],
                                port=info["local_port"], 
                                username=info["local_username"], 
                                password=info["local_passwd"],
                                database=info["db"],
                                ssl=isSSL
                                )
    except Exception as e:
        print("Error: %s" %e)
        exit()
    
    # if the local database already had the database
    for i in client.get_list_database():
        if i['name'] == info["db"]:
            dbExisted = True
            break
            
    # create new database if it doesn't existed.
    if not dbExisted:
        print("database {} doesn't existed. Creating a new one...".format(info["db"]))
        client.create_database(info["db"])
        return [], readSuccess

    field_list = ''
    for i in info["fields"]:
        field_list += i + ','
    field_list = field_list[:-1]

    sTime, eTime = datetime_convert(info["startUTCTime"], info["endUTCTime"])
    sTime_str = str(int((sTime.timestamp()*1000)*1000000))
    eTime_str = str(int((eTime.timestamp()*1000)*1000000))
    
    query = 'SELECT ' + field_list + "::field, " +"case::tag "+ "FROM " + info["measurement"] + ' WHERE time > ' + sTime_str + ' and time < ' + eTime_str
    result = client.query(query)
    data = list(result.get_points())
    
    if not data:
        return readSuccess
    # return client, dbExited
    readSuccess = True
    return data, readSuccess



# How should I know if the local database is up-to-date?
def read_data(info=src_info.copy()):

    data, status = read_localDB()
    if status:
        print("Reading successfully from local DB")
        return data
    
    print("No requested data in local DB...then reading from remote DB")
    
    data = read_remoteDB(src_info.copy())
    return data
    

def main():
    # test if required programs are installed
    test_software_installed()
    # the return data
    data = read_data(src_info.copy())
    return


if __name__ == "__main__":
    main()