
# https://roboticsbackend.com/raspberry-pi-arduino-serial-communication/#Serial_via_USB
# This is an experimental program to read serial data from an arduino through usb
from time import sleep, strftime, time
import serial
import time

# initialize serial arduino object
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=0.1)
arduino.flush()  # Clear input and output buffer

# Enable temp readings
from gpiozero import CPUTemperature

#promt user for log file name
logFile = "log.csv" #default
logFile = input("File to save data to: ")
log = open(logFile, 'a')
print("Logging data to '" + logFile + "'..." )

while True:
    try:
        data = arduino.readline().decode('utf-8').strip() # decode serial bytes and remove trailing characters (\n)
    except UnicodeDecodeError:
        data = "invalid characters revieved"
    cpu = CPUTemperature()
    temp = str(cpu.temperature)
    message = str("Trial on: ")
    dateYMD = strftime("%Y-%m-%d")
    timeHMS = strftime("%H:%M:%S")
    print(data)
    log.write("{0},{1},{2},{3},{4}\n".format(message,dateYMD,timeHMS,str(data),temp))
    time.sleep(0.001)
