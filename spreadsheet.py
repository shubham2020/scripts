import gspread
from oauth2client.service_account import ServiceAccountCredentials

import serial
import datetime
import time


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('Cred3.json', scope)
client = gspread.authorize(creds)

ser = serial.Serial('/dev/ttyACM0',9600)
bfl = 1

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("sensorValue").sheet1

# Extract and print all of the values
#list_of_hashes = sheet.get_all_records()
#print(list_of_hashes)
count = 1

while(count <= 10):

	read_serial=ser.readline()
	pressure = str(int (ser.readline(),16))

	row = [str(datetime.datetime.now()),'Pressure', pressure, 'Brake Fluid Level', bfl]

	#curr_rows = sheet.row_count
	#print(curr_rows)
	#next_row = curr_rows + 1
	sheet.insert_row(row)
	
	count = count + 1
	time.sleep(10)
