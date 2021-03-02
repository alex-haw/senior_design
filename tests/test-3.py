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
# rmf9x.signal_bandwdith = 125000 # default is 125000 (Hz), 125000 is used in long range 
                                  # Signal_bandwdith can be 7800, 10400, 15600, 20800, 31250, 41700, 62500, 125000, 250000
# rfm9x.coding_rate = 5 # Default is 5, can be 5,6,7,8
                        # Coding_rate (CR) can be be set higher for better noise tolerance, and lower for increased bit rate
# rfm9x.spreading_factor = 7 # default is 7, higher values increase the ability to distingish signal from noise
                             # lower values increase data transmission rate
 
prev_packet = None
files = os.listdir('transmit_directory/')
currentfile = files[0]
i = 0


while True:

    packet = None
    # draw a box to clear the image
    display.fill(0)
    display.text('RasPi LoRa', 35, 0, 1)

    # check for packet rx
    packet = rfm9x.receive()
    if packet is None:
        display.show()
        display.text('- Waiting for PKT -', 15, 20, 1)
    else:
        # Display the packet has been received and rssi
        display.fill(0)
        prev_packet = packet
        packet_text = str(prev_packet, "utf-8")
        display.text('RX: ', 0, 0, 1)
        display.text('Packet received', 25, 0, 1)

        w = open('receivedfile', 'w')
        w.write(packet_text)
        time.sleep(1)

    if not btnSend.value:
        # Send Chosen File
        display.fill(0)

        # take data from file instead of regular text
        f = open(currentfile, 'r')
        button_a_data = bytes(f.read(), "utf-8")
        rfm9x.send(button_a_data)

        # find a way to insert text into a separate file instead of display
        display.text('Sent File!', 25, 15, 1)

    elif not btnNext.value:
        # Move to next file option
        display.fill(0)

        # set file to open to next tile
        i+=1
        button_next_file = files[i]
        currentfile = button_next_file

        # display possible file to open
        display.text(button_next_file, 25, 15, 1)

    elif not btnPrev.value:
        # Move to previous file option
        display.fill(0)

        # set file to open to previous file
        i=-1
        button_prev_file = files[i]
        currentfile = button_prev_file

        # display possible file to open
        display.text(button_prev_file, 25, 15, 1)

    display.show()
    time.sleep(0.1)
