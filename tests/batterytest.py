# this is used to not log distance
"""
Example for using the RFM9x Radio with Raspberry Pi.

Learn Guide: https://learn.adafruit.com/lora-and-lorawan-for-raspberry-pi
Author: Brent Rubell for Adafruit Industries

This code is tested and works
"""
# Import Python System Libraries
from time import sleep, strftime, time
import time
# Import Blinka Libraries
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import the SSD1306 module.
import adafruit_ssd1306
# Import RFM9x
import adafruit_rfm9x

# set up temp monitor
from gpiozero import CPUTemperature
#enable temp readings
from gpiozero import CPUTemperature



# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)
# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power = 23
# rmf9x.signal_bandwdith = 125000 # default is 125000 (Hz), 125000 is used in long range 
                                  # Signal_bandwdith can be 7800, 10400, 15600, 20800, 31250, 41700, 62500, 125000, 250000
# rfm9x.coding_rate = 5 # Default is 5, can be 5,6,7,8
                        # Coding_rate (CR) can be be set higher for better noise tolerance, and lower for increased bit rate
# rfm9x.spreading_factor = 7 # default is 7, higher values increase the ability to distingish signal from noise
                             # lower values increase data transmission rate
prev_packet = None

# log setup
logFile = "log.csv" # save to log.csv without requiring input, default
#logFile = input("File to save data to: ") # use for asking user what file to write to
log = open(logFile, 'a') # w = overwrite file, a = append, depends on if you want to clear log each time or not
log.write("#status,#date,#time,#minutes passed (minutes),#temp (C),#RSSI (dBm)\n") # column label header if overwriting
print("Logging data to " + logFile + "..." ) # tell user what program is doing
distance = 0 # set distance to zero cause we are not logging distance now

count = 0
while True:
    # get log data
    cpu = CPUTemperature()
    temp = str(cpu.temperature)
    message = str("Total minutes passed: " + str(count))
    dateYMD = strftime("%Y-%m-%d")
    timeHMS = strftime("%H:%M:%S")

    # Write log data to log
    print("Writing to log.csv, Total minutes passed: " +str(count))

    log.write("{0},{1},{2},{3},{4},{5}\n".format(message,dateYMD,timeHMS, str(count), temp,str(rfm9x.last_rssi)))
    time.sleep(60)
    count += 1

