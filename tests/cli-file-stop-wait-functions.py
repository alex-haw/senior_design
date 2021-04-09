# this is a modified version of cli-file-stop-wait.py that is broken into functions. 
# send specific files over lora
# Currently working on parsing
# Import Python System Libraries
import time
# Import Blinka Libraries
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import math
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

# file setup
files = os.listdir("tx_dir") # get files from this directory
currentfile = files[0]
i = 0 # variable for listing files
receivedfile = "rfile.txt" # default file to write to
open("rx_dir/" + receivedfile,"w").close() # open file and close to clear it when program starts

# Global variable declarations
header = None # holds packet number, size defined by header_size  
data = None # holds data, size us up to chunk_size
routing_flags = "0x000"
pkt_num = "0x00"
max_pkt_size = 250 # maximum amount of bytes that can be send in a packet, it is 251B
pkt_num_size =   2 # 2 Hex chararters for pkt num
routing_flags_size  = 3 # 3 Hex characters: 1=Routing #, 2=Pi# Send, 3=Pi Receive#
header_size = pkt_num_size + routing_flags_size
chunk_size   = max_pkt_size - header_size # chunk size in Bytes, maximum size of data
file_too_big = False
packet_size_error = False
too_many_tries = False
#sent_size = 0
file_size = 0

########################################### Function Declarations #######################################################
# TX FUNCTIONS
def incPktNum(pkt_num): # increment packet num from string back to string ( "0x00" -> "0x01") 
    pkt_num = int(pkt_num,16)  # Convert pkt_num from hex    to int
    pkt_num += 1  # Incrment pkt_num
    pkt_num = hex(pkt_num) # convert from int to hex
    pkt_num = str(pkt_num) # convert to string, includes "0x"
    pkt_num = pkt_num[2:] # get rid of "0x"
    pkt_num = pkt_num.zfill(header_size) # fit digits to header size
    pkt_num = "0x" + pkt_num # add 0x back
    return pkt_num

def ask_user_what_file_to_send(): # Function returns a file name selected by the user
    file_too_big = True # set to true so that it does the loop at least once
    while file_too_big == True:
        print("The current files in tx_dir/ are:") # List Files in Transmit Directory And ask user what fil to send
        for x in range(len(files)): # show all files
            print(str(x+1) + ": " + files[x])
        print("\n")
        option = input("Enter a Number: ")
        selected_file = files[int(option)-1]
        file_too_big, file_size =  check_file_size(selected_file) # See if file is too big
        #file_too_big = True
    print(" you have selected" + selected_file)
    return selected_file, file_too_big, file_size

def check_file_size(file_name): # Makes Sure files are smoll enough, sets file_too_big
    file_too_big = False
    file_size = os.stat("tx_dir/" + file_name).st_size # get file size in bytes
    max_num_of_packets = (16**pkt_num_size) # calc maximum number of packets than can be sent, a**b =a^b
    num_of_chunks = file_size/chunk_size
    max_file_size = max_num_of_packets * chunk_size
    file_too_big = packet_size_error = False # Errors for if the file is too big, and if packets are too big
    if (num_of_chunks > max_num_of_packets): # If the amount of packets exceeds pkt_num range
        file_too_big = True # do not send file by skipping the next while loop
    print("It will take at least " + str(math.ceil(num_of_chunks)) + " packets to send " + file_name) # rounds up
    print("Pausing for 2 seconds...")
    time.sleep(2) # Give user 4 seconds to see if the file will take too long to send
    return file_too_big, file_size

def send_file(file_name, file_too_big, file_size): # handels all aspects of sending an entire file
    print("START OF SEND_FILE")
    f = open("tx_dir/" + currentfile, "r") # open file, changed to reading bytes cause sotemise its bigger
    sent_size = 0 # clear sent_size for new file
    pkt_num = "0x01"
    too_many_tries = False
    packet_size_error = False

    while sent_size < file_size and file_too_big == False and too_many_tries == False:
        print("Getting Chunk, beginning packet sending shortly ")
        data = f.read(chunk_size) # read chunk of file for data
        header = pkt_num[-header_size:] # get last characters from pkt-num
        tx_data = header + data # add header and data
        print("The full packet (tx_data) is: " + tx_data)
        tx_data = bytes(tx_data,"utf-8") # format data for packet
        too_many_tries, packet_size_error = sendPacketForFile(tx_data, pkt_num)
        if too_many_tries:
            print("No ACK, too many failed attempt to send a packet")

        # Increment pkt_num with string format for next packet
        print("pkt_num is currently " + pkt_num[-header_size:]) # print last charaters
        pkt_num = incPktNum(pkt_num) # takes string, adds one, converts pack to string
        print("pkt_num is now " + pkt_num[-header_size:] + "\n") # print last two characters (hex Digits) from pkt_num

        # Increase sent size (assume packet was sent for now)
        sent_size = sent_size + chunk_size # print("sent_size is now: " + str(sent_size)) 
        # Go back to     while sent_size < file_size:
    if sent_size >= file_size:
        tx_data = pkt_num = "0x00"
        tx_data = bytes(tx_data,"utf-8") # format data for packet
        sendPacketForFile(tx_data, pkt_num)
    print("END OF SEND_FILE")
    return too_many_tries, packet_size_error

def sendPacketForFile(tx_data, pkt_num): # Send 1 packet and check for ACK, resend if necasary
    print("	START OF SENDPACKETFORFILE")
    packet_size_error = False
    too_many_tries = False
    packet = None # Clear packet in order to check for one.
    tries = 0; # clear tries for next send
    if len(tx_data) > 252: # If a Unicode character is encountered, it might not fit into a byte
        packet_size_error = True # Stop sending the file

    #packet = True # Uncomment to skip the following loop.
    rfm9x.send(tx_data) # Send data
    while tries < 3 and packet is None and packet_size_error == False: # try sending 3 times
        print("    Checking for ACK, pausing for 5 seconds")
        packet = rfm9x.receive(timeout = 5) # Wait for 5 seconds for receiever to request packet
        if packet is None: # If no packet received
            print("No ACK, Resending packet number " + pkt_num)
            rfm9x.send(tx_data) # send packet again
            tries += 1 # incement tries
        else: # IF a packet is received
            packet_txt = str(packet,"utf-8") #convert packet to string, should have two characters
            print("Ack Received")
            if packet_txt == pkt_num[-header_size:]: # if the received packet is equal to packet_num
                print("Error in received pkt, resending")
                rfm9x.send(tx_data) # send packet gain
                tries += 1
                packet = None # empty packet to start try loop again
            else: # If the packet is not equal to pkt_num, assume receiver wants next packet for now
                continue # do nothing
            # go back to start of try sending 3 times unless the packet =/= pkt_num
    if tries >= 3:
        too_many_tries = True
        print("Too Many Tries")
    print("	END OF SENDPACKTEFORFILE")
    return too_many_tries, packet_size_error
    # at this point, the function has ceased trying to send a packet, wether there was an error or not

def TX_errors(too_many_tries,file_too_big,packet_size_error): # prints errors
    if too_many_tries:
        print("ERROR:, too many failed attepmts to send file, the file was not fully sent")
    elif file_too_big:
        print("ERROR: FILE TOO BIG! File size of " + str(file_size) + " exceeds "+ str(max_file_size) + " byte max")
    elif packet_size_error:
        print("ERROR: too many bytes, please reduce max_pkt_size to send this file or remove Unicode characters")
    else: # if no error
        print(" FILE HAS FINISHED SENDING with NO ERRORS  *********************************************** ")

# RX Functions
def receive_a_file():
    received = False
    w = open("rx_dir/" + receivedfile, "a")
    pkt_num = "0x01" # start with packet number zero
    next_pkt_num_request = "0x01" # start with zero
    wait = True
    packet = idle_RX(wait)
    if packet is None:
        print("no packet received")
    else: # If a packet is recieved, enter data  RX mode
        valid_pkt = check_rec_pkt(packet)
        if valid_pkt:
            # try: # Try to recieve unless there is an error at any point in the rest of this try portion, ignore for now
            pkt_num, received = keep_receiving_packets(packet,file,pkt_num) # functions
            print("Recieved has timed out for 25 seconds \n The file has either been fully recieved or the sender stopped sending")
            if received:
                print("The file was received with no errors")
            else:
                print("The file was not fully recieved")
        else:
            print("An invalid packet was received and will be ignored")
    print("END OF RECIEVEAFILE")
    return received

def check_rec_pkt(rec_pkt):
    valid = True # asume it is valid for now
    # convert to string
    # get flags
    # if flags do not match destination
    return valid

def keep_receiving_packets(packet,file,pkt_num):
    while packet is not None: # Keep going as long as packets are recieved
        packet_text = str(packet, "utf-8") # get string from packet
        pkt_num_rec = packet_text[0:2] # get first two characters for packet number
        pkt_num_rec = int(pkt_num_rec,16)  # convert first two bytes to int from recieved pkt
        packet_text = packet_text[2:] # get data from packet
        if pkt_num_rec == pkt_num[2:]: # compare hex digits to the pkt_number without "0x"
            print("Recieved Packet number: " + str(pkt_rec) + " Writing to " + receivedfile + " now")
            file.write(packet_text)
            next_pkt_request = incPktNum(pkt_num) # get next packet number
            next_pkt_request = bytes(next_pkt_request,"utf-8") #convert next_pkt_request to bytes
            print("Requesting Next Packet")
            rfm9x.send(next_pkt_request)
        elif pkt_num_rec == "00":
            received = True
            # close file
        else: # if the recieved packet number was not what RX was expecting
            rfm9x.send(bytes(next_pkt_request[2:],"utf-8")) # request the next packet from hex digits only
        packet = None
        print("Waiting for packet #" + str(pkt_number))
        packet = rfm9x.receive(timeout = 25) # wait 25 seconds before assuming the sender as quit sending
    return pkt_num, received

def idle_RX(wait): # receives a packet, either once or forever
    if wait == True: # wait until a packet is received
        packet = None
        while packet is None:
            print("Waiting for packet for 5 seconds")
            packet = rfm9x.receive(timeout = 5) #
    else: 
        packet = rfm9x.receive(timeou = 5) # wait for 5 seconds
    return packet

########################################### Start of Top Interface ######################################################
print("Please Choose a Mode: \n RX=1\n TX=2\n")
choice = input("Enter Number:")

while int(choice) == 1: # RX mode
    receive_a_file() # waits for a packet and then decides whether or not to write packet to file
    print("END OF RX MODE")

while int(choice) == 2: # TX Mode
    current_file, file_too_big, file_size = ask_user_what_file_to_send() # Returns selected_file name and file_too_big
    too_many_tries = send_file(current_file,file_too_big,file_size) # Sends file, returns True if too many attempts occured
    TX_errors(too_many_tries,file_too_big,packet_size_error) # display errors
    print(    "__________END OF FILE SENDING___________________________") # better show the restart of TX mode
    time.sleep(1) # Pause for 1 second, go back to asking user for file to send

while True: # End Idle Mode (optional if a break in the TX mode)
    print("An ERROR has occured, One of the modes has been exited please restart program")
    time.sleep(5)
