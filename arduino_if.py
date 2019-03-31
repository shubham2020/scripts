# Google Spreadsheet access specific libraries
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# raspberry pi specific libraries
import RPi.GPIO as GPIO
import time

# arduino specific libraries
import serial

# For adding time stamp to the sensor data
import datetime

# thread import 
import threading


class mainCode:
	
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	
	def __init__(self): #initializing the objects and pins for raspberry pi
		
		#object for setting up arduino port and baud rate
		self.ser = serial.Serial('/dev/ttyACM0',9600)
		
		#pins' setup for checking the interrupt for the brake fluid level 
		self.first_pin = 40
		self.second_pin = 38
		GPIO.setup(self.first_pin, GPIO.OUT)
		GPIO.setup(self.second_pin, GPIO.IN)
		
		#switches for logic of development to take readings
		self.sc_in = 8
		self.sc_out = 10
		self.tyre_in = 33
		self.tyre_out = 31
		GPIO.setup(self.sc_in, GPIO.OUT)
		GPIO.setup(self.sc_out, GPIO.IN)
		GPIO.setup(self.tyre_in, GPIO.OUT)
		GPIO.setup(self.tyre_out, GPIO.IN)
		
		#Google spreadsheet access setup of authorization
		scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
		creds = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/scripts/Cred3.json', scope)
		client = gspread.authorize(creds)
		
		#initializing sheet object
		self.sheet = client.open("sensorValue").sheet1
		
		#global variables 
		self.bfl = 0 # Brake fluid level indicator
		self.press_Val = [] # to store 4 tyre values
		
	def _pressureRead(self): # reading the pressure sensor
		read_serial=self.ser.readline()
		value = str(int (self.ser.readline(),16))
		
		return value
		
	def _reservoirRead(self): #reading the reservoir fluid level
		GPIO.output(self.first_pin, GPIO.HIGH)
		if GPIO.input(self.second_pin) == True:
			return 1
		else:
			return 0
			
	def readReservoirStatus(self):	#read reservoir if switch is on
		GPIO.output(self.sc_in, GPIO.HIGH)
		while True:	
			if GPIO.input(self.sc_out) == True:
				print ('reading reservoir!!!!!!!')
				self.bfl = self._reservoirRead()
				return self.bfl
			else:
				pass
			
	def readTyrePressure(self):	#To read the tyre pressure if the switch is on
		GPIO.output(self.tyre_in, GPIO.HIGH)
		for i in range(4):
			while True:
				if GPIO.input(self.tyre_out) == True:
					print('reading tyre pressure!!!!!!!!')
					self.press_Val.append(self._pressureRead())
					time.sleep(3)
					break
				else:
					pass

if __name__ == '__main__':
	#object of the class
	obj = mainCode()
	
	thread1 = threading.Thread(target = obj.readReservoirStatus) #thread to read reservoir status
	thread2 = threading.Thread(target = obj.readTyrePressure)	# thread to read tyre pressure
	
	thread1.start()
	thread2.start()
	
	thread1.join()
	thread2.join()
	
	row = [str(datetime.datetime.now()), 'Brake Fluid Level', obj.bfl]
	obj.sheet.insert_row(row)
    
	for i in range(4):
		row = [str(datetime.datetime.now()),('tyre'+str(i+1)), obj.press_Val[i]]
		obj.sheet.insert_row(row)
		
	GPIO.cleanup()

		
		
