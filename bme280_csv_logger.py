#!/usr/bin/python3
'''
Mix of different tutorials, including https://bit.ly/343VgAM
TEMP SENSOR = adafruit_bme280 - https://bit.ly/3svubRT
	*Temp Sensor Note* NOT THE bmp280 (no humidity), use BME280
'''
import RPi.GPIO as GPIO                         # Import GPIO
import os
import sys
import datetime				# for Dates
from datetime import date	# for Dates
import csv
from csv import writer
import pytz 				# https://bit.ly/3xw7for (pip install pytz)
import collections
import math
import json
from gpiozero import CPUTemperature   # Calls out the CPU temp sensor
from adafruit_bme280 import basic as adafruit_bme280 # pip3 install adafruit-circuitpython-bme280
i2c = board.I2C()  # uses board.SCL and board.SDA for BME280
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

utcnow = datetime.datetime.now(tz=pytz.UTC) #create UTC datetime
mstnow = utcnow.astimezone(pytz.timezone('US/Mountain'))  #create MST datetime
dtLocal = mstnow.replace(microsecond=0, tzinfo=None) #remove microseconds and UTC num
dtUtc = utcnow.replace(microsecond=0, tzinfo=None) #remove microseconds and UTC num
UTCformat = (dtUtc.strftime("%Y-%m-%d %H:%M:%S"))  # put D/T into YYYY-MM-DD HH:MM:SS

dateOnly = date.today() # call just standard today
timeOnly = dtLocal.strftime("%H:%M:%S") # pull just time from D/T
month = datetime.datetime.now().strftime("%Y-%m(%B)")

temp_file = ('/home/pi/myscripts/logger/%s-log-temp_readings.csv' % month)
temp_json = ('/home/pi/allsky/config/overlay/extra/internals.json')
#mag_file = ('/home/pi/myscripts/logger/%s-log-mag_readings.csv' % month)

# Temperature readings from BME280
def bme_temp_csv():
	cpu = CPUTemperature()
	cpuTempL = float((cpu.temperature) * 9 / 5 + 32.001)    # Calls out CPU Temp and converts to Fahrenheit
	cpuTempF = round(cpuTempL, 1)
	pressureRaw = bme280.pressure
	pressureCal = pressureRaw  - 886.001
	pressure = round(pressureCal, 3)
	intHumRaw = bme280.relative_humidity
	intHum = round(intHumRaw, 1)
	intTemp = bme280.temperature
	intTempF = float((intTemp) * 9 / 5 + 32.001)
	intTempF = round(intTempF, 1)
	b = 17.62
	c = 243.12
	gamma = (b * bme280.temperature /(c + bme280.temperature)) + math.log(bme280.humidity / 100.0)
	dewpoint = (c * gamma) / (b - gamma)
	dp = round(dewpoint, 3)
	temp_data = {'LocalDate':str(dateOnly), 'LocalTime':str(timeOnly),  'UTC':str(UTCformat), 'cpuTempF':cpuTempF, 'intTempF':intTempF, 'intHum':intHum, 'pressure':pressure, 'dewpoint':dp}

	if os.path.isfile(temp_file): #checks if file exists. if yes, appends values for dictionary under corresponding header in a new line
		with open(temp_file, 'a', newline='') as csvfile:
			fieldnames = ['LocalDate', 'LocalTime', 'UTC', 'cpuTempF', 'intTempF', 'intHum', 'pressure', 'dewpoint']
			data_writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')#, quotechar='|', quoting=csv.QUOTE_MINIMAL)
			data_writer.writerow({'LocalDate': temp_data['LocalDate'], 'LocalTime': temp_data['LocalTime'], 'UTC': temp_data['UTC'], 'cpuTempF': temp_data['cpuTempF'], 'intTempF': temp_data['intTempF'], 'intHum': temp_data['intHum'], 'pressure': temp_data['pressure'], 'dewpoint': temp_data['dewpoint']})
	else: #creates file (that has been checked and does not yet exist) and adds headers and values for all keys in dict
		with open(temp_file, 'w', newline='') as csvfile:
			fieldnames = ['LocalDate', 'LocalTime', 'UTC', 'cpuTempF', 'intTempF', 'intHum', 'pressure', 'dewpoint']
			data_writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')#, quotechar='|', quoting=csv.QUOTE_MINIMAL)
			data_writer.writeheader()
			data_writer.writerow({'LocalDate': temp_data['LocalDate'], 'LocalTime': temp_data['LocalTime'], 'UTC': temp_data['UTC'], 'cpuTempF': temp_data['cpuTempF'], 'intTempF': temp_data['intTempF'], 'intHum': temp_data['intHum'], 'pressure': temp_data['pressure'], 'dewpoint': temp_data['dewpoint']})
	# Data to be written to JSON FILE for AllSky Variables
	dictionary = {
		"INT_CPU_TEMPF": cpuTempF,
		"INT_HUM": intHum,
		"INT_TEMPF": intTempF
	}
	# Serializing json
	json_object = json.dumps(dictionary, indent=4)
	# Writing to temp_json file
	with open(temp_json, "w") as outfile:
		outfile.write(json_object)
	#print(temp_data)


bme_temp_csv()
