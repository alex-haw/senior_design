# send specific files over lora
# Currently working on parsing
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
# rmf9x.signal_bandwdith = 125000 # default is 125000 (Hz), 125000 is used in long range
                                  # Signal_bandwdith can be 7800, 10400, 15600, 20800, 31250, 41700, 62500, 125000, 250000
# rfm9x.coding_rate = 5 # Default is 5, can be 5,6,7,8
                        # Coding_rate (CR) can be be set higher for better noise tolerance, and lower for increased bit rate
# rfm9x.spreading_factor = 7 # default is 7, higher values increase the ability to distingish signal from noise
                             # lower values increase data transmission rate
prev_packet = None
files = os.listdir("tx_dir") # get files from this directory
currentfile = files[0]
i = 0
open("rx_dir/receivedfile.txt","w").close() # open file and close to clear it when program starts

print("Please Choose a Mode: \n RX=1\n TX=2\n")
choice = input("Enter Number:")

while int(choice) == 1: # RX Mode
    packet = None
    # check for packet rx
    packet = rfm9x.receive(timeout=5) # wait for recieve for timout duration.
    if packet is None:
        print("Waiting for Packet")
    else:
        # Display the packet has been received and rssi
        prev_packet = packet
        packet_text = str(prev_packet, "utf-8")
        print("Packet Received, Writing to 'receivedfile' now")
        w = open("rx_dir/receivedfile.txt", "a") 
        w.write(packet_text)
        time.sleep(1)

while int(choice) == 2: # TX Mode
    # List Files in Transmit Directory
    print("The current files in tx_dir/ are:")
    for x in range(len(files)): # show all files
        print(files[x])
    print("\n")
    # Ask User to Choose a File
    currentfile = input("What file would you like to open? (include .txt)")

    # Show Chosen File
    #print("The contents of " + currentfile +" is:\n")
    #f = open("tx_dir/" + currentfile, "r")
    #for line in f:
    #    print(line)

    filesize = os.stat("tx_dir/" + currentfile).st_size # get file size in bytes
    if filesize > 252:
        print("***** File size exceeds packetsize, multiple packets will be sent *****\n")
        print("***** This function has not been created yet")
        # Parse files
        #sentsize = 0 # variable to keep track of how much data has been sent
        #f = open("tx_dir/" + currentfile,"r")
        #while sentsize < filesize :
             # get first 251 bytes
             # send it through LoRa
             # add 251 to sent size
    else:
        # Send contents with one packet
        print(currentfile + " is now being sent through LoRa\n")
        f = open("tx_dir/" + currentfile, 'r')
        tx_data = bytes(f.read(), "utf-8")
        rfm9x.send(tx_data)
    time.sleep(0.1)
