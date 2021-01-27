# send specific files over lora

# Import Python System Libraries
import time
# Import Blinka Libraries
import busio
from digitalio import DigitalInOut, Direction, Pull
import board

# Import RFM9x
import adafruit_rfm9x
import os

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power = 23
prev_packet = None
files = os.listdir('transmit_directory/')
currentfile = files[0]
i = 0

print("Please Choose a Mode: \n RX=1\n TX=2\n")
choice = input("Enter Number:")

while int(choice) == 1:
    packet = None

    # check for packet rx
    packet = rfm9x.receive()
    if packet is None:
        print("Waiting for Packet")
    else:
        # Display the packet has been received and rssi
        prev_packet = packet
        packet_text = str(prev_packet, "utf-8")
        print("Packet Received")
        w = open('receivedfile', 'w')
        w.write(packet_text)
        time.sleep(1)

while int(choice) == 2:
    
    # List Files in Transmit Directory
    print("** The current files in transmit_directory/ are:")
    for x in range(len(files)):
        print(files[x])

    # Ask User to Choose a File
    print("What file would you like to open?")
    currentfile = input()

    # Show Chosen File
    print("The contents of " + currentfile +" is:\n")
    f = open("transmit_directory/" + currentfile, "r")
    for line in f:
        print(line)

    # Send Chosen File
    f = open("transmit_directory/" + currentfile, 'r')
    tx_data = bytes(f.read(), "utf-8")
    rfm9x.send(tx_data)

    # find a way to insert text into a separate file instead of display
