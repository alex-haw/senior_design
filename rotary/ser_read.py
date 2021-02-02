# https://roboticsbackend.com/raspberry-pi-arduino-serial-communication/#Serial_via_USB
# This is an experimental program to read serial data from an arduino through usb
import serial, time
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout = 0.1) # initialize serial arduino object
arduino.flush() # Clear input and output buffer

# Enable temp readings
from gpiozero import CPUTemperature

f = open('log.csv', 'a')

while True:
	#data = arduino.readline().decode('ascii').rstrip() # decode serial bytes and remove trailing characters (\n)
	#if data:
	#print(data)
	# LOG DATA
#	cpu = CPUTemperature()
#	temp = str(cpu.temperature)
#	date = strftime("%Y-%m-%d %H:%M:S")
#	log.write("{0},{1}/n".format(date,temp))
	time.sleep(1)
