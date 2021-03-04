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

# file setup
files = os.listdir("tx_dir") # get files from this directory
currentfile = files[0]
i = 0 # variable for listing files
receivedfile = "rfile.txt" # default file to write to
open("rx_dir/" + receivedfile,"w").close() # open file and close to clear it when program starts

pkt_num_int = 0
next_pkt_request = 0

header = None # holds packet number, size defined by header_size  
data = None # holds data, size us up to chunk_size
# => tx_data = header + data

max_pkt_size = 250 # maximum amount of bytes that can be send in a packet, it is 251B
header_size  =   3 # Size of header that holds packet number, 2 bytes gives up to 256 packets
                   # each bytes gives one character for hex
chunk_size   = max_pkt_size - header_size # chunk size in Bytes, maximum size of data

print("Please Choose a Mode: \n RX=1\n TX=2\n")
choice = input("Enter Number:")


while int(choice) == 1: # RX Mode
    w = open("rx_dir/" + receivedfile, "a")
    pkt_number = 0
    packet = None
    print("Waiting to recieve for 5 seconds")
    packet = rfm9x.receive(timeout=5) # wait 5 seconds for reciever timeout
    if packet is None: # idle RX mode
        print("Waiting for Packet")
    else: # If a packet is recieved, enter data  RX mode
        while packet is not None: # Keep going as long as packets are recieved
            packet_text = str(packet, "utf-8")
            pkt_rec = packet_text[0:header_size] # get first two characters for packet number
            pkt_rec = int(pkt_rec,16)  # convert first two bytes to int
            packet_text = packet_text[header_size:] # get data from packet
            if pkt_rec == pkt_number:
                # Write data to file
                print("Recieved Packet number: " + str(pkt_rec) + " Writing to " + receivedfile + " now")
                w.write(packet_text)
                # Request Next Packet
                pkt_number += 1
                next_pkt_request = pkt_rec + 1 # integer
                next_pkt_request = hex(next_pkt_request)
                next_ptk_request = str(next_pkt_request)
                next_pkt_request = bytes(next_pkt_request,"utf-8")
                print("Requesting Next Packet")
                #time.sleep(1); # removed this sleep to make it faster, still sends large files when commented
                rfm9x.send(next_pkt_request);
            else: # if the recieved packet number was not what RX was expecting
                rfm9x.send(next_pkt_request);
            packet = None
            print("Waiting for packet #" + str(pkt_number))
            packet = rfm9x.receive(timeout = 25) # wait 25 seconds before assuming the sender as quit sending
        print("Recieved has timed out for 25 seconds \n The file has either been fully recieved or the sender stopped sending")

######### Transmit Mode
while int(choice) == 2: # TX Mode
    print("The current files in tx_dir/ are:") # List Files in Transmit Directory And ask user what fil to send
    for x in range(len(files)): # show all files
        print(str(x+1) + ": " + files[x])
    print("\n")
    option = input("Enter a Number: ")
    currentfile = files[int(option)-1]
    file_size = os.stat("tx_dir/" + currentfile).st_size # get file size in bytes
    f = open("tx_dir/" + currentfile, "r") # open file, changed to reading bytes cause sotemise its bigger

    # Skip sending if there are not enough bits
    max_num_of_packets = (16**header_size) # calc maximum number of packets than can be sent, a**b =a^b
    num_of_chunks = file_size/chunk_size
    max_file_size = max_num_of_packets * chunk_size
    file_too_big = packet_size_error = False
    if (num_of_chunks > max_num_of_packets):
        file_too_big = True # do not send file by skipping the next while loop
    print("It will take at least " + str(num_of_chunks) + " packets to send " + currentfile)
    sent_size = 0
    #pkt_num = "0x00"
    pkt_num = "0" # start with packet 0
    pkt_num = "0x" + str(pkt_num.zfill(header_size)) # force the number of digits to header size, add 0x 
    tries = 0

    while sent_size < file_size and file_too_big == False:
        # get data from chunk of file
        print("Getting Chunk, beginning packet sending shortly ")
        data = f.read(chunk_size) # read chunk of file for data
        #data = str(data,"utf-8") # sometimes the data will exced chunk size, uncomment this to stop
        header = pkt_num[-header_size:] # get last characters from pkt-num
        tx_data = header + data # add header and data
        print("The full packet (tx_data) is: " + tx_data)
        tx_data = bytes(tx_data,"utf-8")
        # Send 1 packet and check for ACK, resend if necasary
        packet = None # Clear packet in order to check for one.
        tries = 0; # clear tries for next send
        if len(tx_data) > 252: # I found that sometimes converting to bytes can actuall exceed max LoRa size of 252
            print("Max packet size is " + str(max_pkt_size))
            print("header size is " + str(len(header)))
            print("Data size is " + str(len(data)))
            print("len(tx_data) " + str(len(tx_data)))
            packet_size_error = True
            break # stop trying to send this file
        rfm9x.send(tx_data)

        #packet = True # Uncomment to skip the following loop.
        while tries < 3 and packet is None: # try sending 3 times
            print("    Checking for ACK, pausing for 5 seconds")
            packet = rfm9x.receive(timeout = 10) # Wait for 5 seconds for receiever to request packet
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

        # If no ACK is recieved from reciever after 3 attempts
        if packet is None:
            print("No acknowledge recieved, canceling send")
            break # Exits  [while sent_size < file_size:] and leads to the restart of TX mode
        # At this point it is assumed that the paket was correctly sent and recieved

        # Increment pkt_num with string format for next packet
        print("pkt_num is currently " + pkt_num[-header_size:]) # print last charaters
        pkt_num = int(pkt_num,16)  # Convert pkt_num from hex    to int
        pkt_num += 1  # Incrment pkt_num
        pkt_num = hex(pkt_num) # convert from int to hex
        pkt_num = str(pkt_num) # convert to string, includes "0x"
        pkt_num = pkt_num[2:] # get rid of "0x"
        pkt_num = pkt_num.zfill(header_size) # fit digits to header size
        pkt_num = "0x" + pkt_num # add 0x back
        print("pkt_num is now " + pkt_num[-header_size:] + "\n") # print last two characters (hex Digits) from pkt_num
        time.sleep(2)
        # Increase sent size (assume packet was sent for now)
        sent_size = sent_size + chunk_size
        print("sent_size is now: " + str(sent_size)) 
        # Go back to     while sent_size < file_size:

    # At this Point, the file should be either sent or too many failed attempts to send it occured
    if (tries == 3):
        print("ERROR:, too many failed attepmts to send file, the file was not fully sent")
    elif file_too_big == True:
        print("ERROR: FILE TOO BIG!")
        print("File size of " + str(file_size) + " bytes")
        print("exceeds max. " + str(max_file_size) + " bytes")
    elif packet_size_error == True:
        print("ERROR: Converting to bytes has exceeded LoRa packet size (252), please reduce max_pkt_size to send this file")
    else:
        print(" FILE HAS FINISHED SENDING with NO ERRORS  *********************************************** ")
    print("_____________________________________") # better show the restart of TX mode
    time.sleep(1) # Pause for 1 second, go back to asking user for file to send
    #End of TX mode, go back to start of tx mode

# End Idle Mode (optional if a break in the TX mode
while True:
    print("An ERROR has occured, One of the modes has been exited please restart program **************")
    time.sleep(5)
