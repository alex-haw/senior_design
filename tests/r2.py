# secondtest.py
# This is a modified version of firsttest.py that eliminates the need for buttons and a display
# Made by evan on 01/25/2021
# It is now being used to test range settings to see if they work

"""
Example for using the RFM9x Radio with Raspberry Pi.

Learn Guide: https://learn.adafruit.com/lora-and-lorawan-for-raspberry-pi
Author: Brent Rubell for Adafruit Industries

This code is tested and works
"""
# Import Python System Libraries
import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import RFM9x
import adafruit_rfm9x

# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power = 23

# Default Settings
# rmf9x.signal_bandwdith = 125000 # default is 125000 (Hz), 125000 is used in long range 
                                  # Signal_bandwdith can be 7800, 10400, 15600, 20800, 31250, 41700, 62500, 125000, 250000
# rfm9x.coding_rate = 5 # Default is 5, can be 5,6,7,8
                        # Coding_rate (CR) can be be set higher for better noise tolerance, and lower for increased bit rate
# rfm9x.spreading_factor = 7 # default is 7, higher values increase the ability to distingish signal from noise
                             # lower values increase data transmission rate
                             # Valid values are limited to 6, 7, 8, 9, 10, 11, or 12

# Long Range Test 1:
# rmf9x.signal_bandwdith = 125000
# rfm9x.coding_rate = 5
# rfm9x.spreading_factor = 12

# Long Range Test 2:
rfm9x.signal_bandwdith = 62500
# rfm9x.coding_rate = 5
rfm9x.spreading_factor = 12

prev_packet = None

mode = "TX"

while True:
    packet = None
    print("******************")
    print("** Rasppi LoRa  **")  # Print to console
    print("** test-2.py *****")
    bw = rfm9x.signal_bandwidth
    cr = rfm9x.coding_rate
    sf = rfm9x.spreading_factor
    print("With the following settings: ")
    print("    badwith: " +str(bw) +" Hz ")
    print("    coding rate: " +str(cr))
    print("    spreading factor: " + str(sf))

    print("Would you like to this program to TX or RX (TX/RX)")
    mode = input()
    print(str(mode) + " mode has been set")
    print("Please restart program if you would like to change mode")


    while mode == "TX":
        print("Sending 'Hello' ")
        tx_data = bytes("Hello", "utf-8")
        rfm9x.send(tx_data)
        print("Hello sent, pausing for 5 secconds...")
        time.sleep(5)

    while mode == "RX":
        #packet = rfm9x.receive()
        packet = rfm9x.receive(timeout = 2)
        if packet is None:
            print("Waiting for packet")
        else:
            prev_packet = packet
            packet_text = str(prev_packet, "utf-8")
            print("Received: " + packet_text + " with RSSI = " + str(rfm9x.last_rssi))
            time.sleep(1)
