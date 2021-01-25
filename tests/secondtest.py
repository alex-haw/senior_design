# secondtest.py
# This is a modified version of firsttest.py that eliminates
# the need for buttons and a display
# Made by evan on 01/21/2021
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
prev_packet = None

mode = "RX"

while True:
    packet = None
    print("******************")
    print("** Rasppi LoRa  **")  # Print to console
    print("******************")

    print("Would you like to this program to TX or RX (TX/RX)")
    mode = input()
    print(str(mode) + " mode has been set")
    print("Please restart program if you would like to change mode")


    while mode == "TX":
        print("Sending 'Hello' ")
        tx_data = bytes("Hello \r\n", "utf-8")
        rfm9x.send(tx_data)
        print("Hello sent, pausing for 5 secconds...")
        time.sleep(5)

    while mode == "RX":
        packet = rfm9x.receive()
        if packet is None:
            print("Waiting for packet")
        else:
            prev_packet = packet
            packet_text = str(prev_packet, "utf-8")
            print("RX: " + packet_text)
            time.sleep(1)
