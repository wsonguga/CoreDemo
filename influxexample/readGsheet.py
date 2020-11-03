from __future__ import print_function
import pickle
import os.path
import datetime 
import time
import sys
import math
import subprocess

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']




# post function 
def postHTTP(systolic, diastolic, heartrate,respiratoryrate, date, time, ms, ms_start, date_start):
    http_post = "curl -i -XPOST \'%s/write?db=%s\' -u %s:%s --data-binary \'" % (ip, db, user, password)
    ##only for the first row
    
    add_ms = int(ms)-int(ms_start)
    # print("ms", ms)
    date_tmp = str(date_start + add_ms*1000000) # notice six 0s are needed
    # print("date_tmp", date_tmp)
    http_post += "\ncaretaker4,location=%s systolic=%s,diastolic=%s,heartrate=%s,respiratoryrate=%s" %(mac, systolic, diastolic, heartrate, respiratoryrate)
    http_post += " " + date_tmp
    http_post += "\'"

    subprocess.call(http_post, shell=True)

    print(http_post)
    date_conv_tmp = int(date_tmp)/1000000000
    # print("timestamp is :", date_conv_tmp)
    dt_object = datetime.datetime.fromtimestamp(date_conv_tmp)

    # print("time after calculation is ", dt_object)

## Read G-sheets function 
def openGsheets(id, range_name):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=id,
                                range=range_name).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
    
        ##For vital log
        x = values[0]
        print(x)
        ms_start = x[9]
        date = str(datetime.datetime.strptime(x[0], '%d %b %Y'))[:11]
        date_str = date + str(x[1]) # yy-mm-dd hh-mm-ss
        print(date_str)
        date_tamp = datetime.datetime.strptime(date_str,'%Y-%m-%d %H:%M:%S').timestamp()
        date_start = int(date_tamp*10e8)
        http_post = "curl -i -XPOST \'%s/write?db=%s\' -u %s:%s --data-binary \'" % (ip, db, user, password)
        http_post += "\ncaretaker4,location=%s systolic=%s,diastolic=%s,heartrate=%s,respiratoryrate=%s" %(mac, x[2], x[3], x[5], x[6])
        http_post += " " + str(date_start)
        http_post += "\'"
        print(http_post)
        #subprocess.call(http_post, shell=True)
        for row in values[1:-1]:
            # sys, dia, hr, rr, date, time, timestamp
            postHTTP(row[2],row[3],row[5],row[6], row[0],row[1], row[9],ms_start,date_start)

if __name__ == '__main__':

    if len(sys.argv) < 1:
        print("Usage: " + sys.argv[0] + " [IP] [database name] [user] [password] [mac] [GoogleSheetsID] [RangeName]")
        print("Example: " + sys.argv[0] + " https://homedots.us:8086 algtest test sensorweb ca:re:ta:ke:r4:aa 1HcuqHb0PE9RFTt9CjDkR5TPwWHfFJG2S4_Kb090p4GU qili-2_vitals_2020-09-15_01-21-18!2:6827")
        print("open browser to see waveform at grafana: {ip}:3000/d/OSjxFKvGk/caretaker-vital-signs?orgId=1")
        quit()
    if len(sys.argv) >= 2:
        ip = sys.argv[1]
    if len(sys.argv) >= 3:
        db = sys.argv[2]
    if len(sys.argv) >= 4:
        user = sys.argv[3]
    if len(sys.argv) >= 5:
        password = sys.argv[4]
    if len(sys.argv) >= 6:
        mac = sys.argv[5]
    if len(sys.argv) >= 7:
        id = sys.argv[6]
    if len(sys.argv) >= 8:
        rangeName = sys.argv[7]
  
    openGsheets(id, rangeName)
