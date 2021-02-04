
# https://roboticsbackend.com/raspberry-pi-arduino-serial-communication/#Serial_via_USB
# This is an experimental program to read serial data from an arduino through usb
from time import sleep, strftime, time
import serial
import time

# gpio
import digitalio
import board
ready = digitalio.DigitalInOut(board.D22)
ready.direction = digitalio.Direction.OUTPUT

# initialize serial arduino object
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=0.1)
arduino.flush()  # Clear input and output buffer

# Enable temp readings
from gpiozero import CPUTemperature

#promt user for log file name
logFile = "log.csv" #default
#logFile = input("File to save data to: ")
log = open(logFile, 'w') # w = overwire file, a = append
log.write("#message,#date,#time,#distance,#temp\n") # column label header
print("Logging data to '" + logFile + "'..." )
count =1
distance = 0 # default start value

while True:
    ready.value = True
    try:
        distance = arduino.readline().decode('utf-8').strip() # decode serial bytes and remove trailing characters (\n)
    except UnicodeDecodeError:
        distance = "invalid characters revieved"
    ready.value = False
    print("Distance = " + str(distance))
    #cpu = CPUTemperature()
    #temp = str(cpu.temperature)
    #message = str("Trial:")
    #dateYMD = strftime("%Y-%m-%d")
    #timeHMS = strftime("%H:%M:%S")
    #if count >= 150: # only write every second
     #   #print("Distance = " + str(data))
        #log.write("{0},{1},{2},{3},{4}\n".format(message,dateYMD,timeHMS,str(data),temp))
      #  arduino.write(1)
      #  count = 1
    time.sleep(1)
