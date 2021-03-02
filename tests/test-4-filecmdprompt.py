# send specific files over lora

# Import Python System Libraries
import time
# Import Blinka Libraries
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import the SSD1306 module.
import adafruit_ssd1306
# Import RFM9x
import adafruit_rfm9x
import os

# Button Send
btnSend = DigitalInOut(board.D13)
btnSend.direction = Direction.INPUT
btnSend.pull = Pull.UP

# Button Prev
btnPrev = DigitalInOut(board.D19)
btnPrev.direction = Direction.INPUT
btnPrev.pull = Pull.UP

# Button Next
btnNext = DigitalInOut(board.D26)
btnNext.direction = Direction.INPUT
btnNext.pull = Pull.UP

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# 128x32 OLED Display
reset_pin = DigitalInOut(board.D4)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
# Clear the display.

display.fill(0)
display.show()
width = display.width
height = display.height

# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power = 23
prev_packet = None
files = os.listdir('tx_dir')
currentfile = files[0]
i = 0
j = 0
print("Please Choose a Mode: \n RX=1\n TX=2\n")
choice = input("Enter Number:")

while int(choice) == 1:
    packet = None
    # draw a box to clear the image
    display.fill(0)
    display.text('RasPi LoRa', 35, 0, 1)

    # check for packet rx
    packet = rfm9x.receive()
    if packet is None:
        display.show()
        display.text('- Waiting for PKT -', 15, 20, 1)
        print("Waiting for Packet")
    else:
        # Display the packet has been received and rssi
        display.fill(0)
        prev_packet = packet
        packet_text = str(prev_packet, "utf-8")
        display.text('RX: ', 0, 0, 1)
        display.text('Packet received', 25, 0, 1)
        print("Packet Received")
        os.chdir('rx_dir')

        w = open('file' + str(j), 'w')
        w.write(packet_text)
        time.sleep(1)
        os.chdir("..")
        j+=1   
while int(choice) == 2:
    print("Select a file to send")
    i = 1
    for x in files:
        print(str(i) +". " + x)
        i+=1
    # Send Chosen File
    option = input("Enter a Number: ")
    display.fill(0)
    
    currentfile = files[int(option) - 1]
    # take data from file instead of regular text
    os.chdir('tx_dir')
    #f = open('text2.txt','r')
    f = open(currentfile, 'r')
    button_a_data = bytes(f.read(), "utf-8")
    rfm9x.send(button_a_data)

    # find a way to insert text into a separate file instead of display
    display.text('Sent File!', 25, 15, 1)
    print("sent file")
    os.chdir("..")

display.show()
time.sleep(0.1)

