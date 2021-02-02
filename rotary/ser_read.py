# https://roboticsbackend.com/raspberry-pi-arduino-serial-communication/#Serial_via_USB
# This is an experimental program to read serial data from an arduino through usb
from time import sleep, strftime, time
import serial, time
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout = 0.1) # initialize serial arduino object
arduino.flush() # Clear input and output buffer

# Enable temp readings
from gpiozero import CPUTemperature

log = open('log.csv', 'a')

while True:
	data = arduino.readline().decode('ascii').rstrip() # decode serial bytes and remove trailing characters (\n)
	if data:
		print(data)
		#log data
		cpu = CPUTemperature()
		temp = str(cpu.temperature)
		message = str("Trial on: ")
		dateYMD = strftime("%Y-%m-%d")
		timeHMS = strftime("%H:%M:%S")
		print("Writing to log.csv\n")
		log.write("{0},{1},{2},{3},{4}\n".format(message,dateYMD,timeHMS,str(data),temp))
	time.sleep(1)
