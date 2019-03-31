# import many libraries
from __future__ import print_function  
from googleapiclient.discovery import build  
from httplib2 import Http  
from oauth2client import file, client, tools  
from oauth2client.service_account import ServiceAccountCredentials    
import datetime

import serial

# My Spreadsheet ID ... See google documentation on how to derive this
MY_SPREADSHEET_ID = '1GN16w2nXvIt6pmJx_juvrp-XuitQrzfsSWRfePJECL8'
ser = serial.Serial('/dev/ttyACM0',9600)
bfl = 1


def update_sheet(sheetname, pressure, bfl):  
    """update_sheet method:
       appends a row of a sheet in the spreadsheet with the 
       the latest pressure and bfl sensor data
    """
    # authentication, authorization step
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    creds = ServiceAccountCredentials.from_json_keyfile_name( 
            'Cred3.json', SCOPES)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API, append the next row of sensor data
    # values is the array of rows we are updating, its a single row
    values = [ [ str(datetime.datetime.now()), 
         'Pressure', pressure, 'Brake_fluid_level', bfl ] ]
    body = { 'values': values }
    # call the append API to perform the operation
    result = service.spreadsheets().values().append(
                spreadsheetId=MY_SPREADSHEET_ID, 
                range=sheetname + '!A1:E1',
                valueInputOption='USER_ENTERED', 
                insertDataOption='INSERT_ROWS',
                body=body).execute()                     


if __name__ == '__main__':  
    #main()
    read_serial=ser.readline()
    pressure = (int (ser.readline(),16))
    update_sheet("sensorValue", pressure, bfl)
