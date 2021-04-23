 # send specific files over lora
# Currently working on parsing
# Import Python System Libraries
import time
# Import Blinka Libraries
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import random
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
#rfm9x.coding_rate = 8 # Default is 5, can be 5,6,7,8
                        # Coding_rate (CR) can be be set higher for better noise tolerance, and lower for increased bit rate
#rfm9x.spreading_factor = 12 # default is 7, higher values increase the ability to distingish signal from noise
                             # lower values increase data transmission rate
# Long Range Test 1:
 #rmf9x.signal_bandwdith = 125000
 #rfm9x.coding_rate = 5
 #rfm9x.spreading_factor = 12

# Long Range Test 2:
rfm9x.signal_bandwdith = 62500
rfm9x.coding_rate = 5
rfm9x.spreading_factor = 12

# Long Range Test 3:
#rfm9x.signal_bandwdith = 125000
#rfm9x.coding_rate = 8
#rfm9x.spreading_factor = 12

prev_packet = None

# file setup
files = os.listdir("tx_dir") # get files from this directory
currentfile = files[0]
i = 0 # variable for listing files
receivedfile = "rfile.txt" # default file to write to
open("rx_dir/" + receivedfile,"w").close() # open file and close to clear it when program starts

header = None # holds packet number, size defined by header_size  
data = None # holds data, size us up to chunk_size
# => tx_data = header + data
node_num = "1"
all_nodes = "f"
max_pkt_size = 247 # maximum amount of bytes that can be send in a packet, it is 251B
header_size  =   5 # Size of header that holds packet number, 2 bytes gives up to 256 packets
                   # each bytes gives one character for hex
chunk_size   = max_pkt_size - header_size # chunk size in Bytes, maximum size of data

# variables for RX mode (moved to start of RX mode)
#next_pkt_request = 0 # Changed to strings to use functions
#next_pkt_request = "0" # start with packet 0
#next_pkt_request = "0x" + str(next_pkt_request.zfill(header_size)) # force the number of digits to header size, add 0x 

# Function Declarations:
def incPktNum(pkt_num): # increment packet num from string back to string ( "0x00" -> "0x01") 
    if pkt_num == "0xff":
        pkt_num = "0x00"
        return pkt_num
    pkt_num = int(pkt_num,16)  # Convert pkt_num from hex    to int
    pkt_num += 1  # Incrment pkt_num
    pkt_num = hex(pkt_num) # convert from int to hex
    pkt_num = str(pkt_num) # convert to string, includes "0x"
    pkt_num = pkt_num[2:] # get rid of "0x"
    pkt_num = pkt_num.zfill(2) # fit digits to header size
    pkt_num = "0x" + pkt_num # add 0x back
    print("packet num = " + pkt_num)
    return pkt_num

def request(file_choice, source_addr): # RX Mode
    w = open("rx_dir/" + file_choice, "a")
    print("sending routing number")
    rfm9x.send(bytes("1"+ source_addr + node_num + "00"+ file_choice,"utf-8"))
    pkt_number = "0x00" # force the number of digits to header size, add 0x
    next_pkt_request = "00" # start expecting with packet 0
    next_pkt_request = "0x"+ "3" + source_addr + node_num + next_pkt_request # force the number of digits to header size, add 0x 
    packet = None
    print("Waiting to recieve for 5 seconds")
    packet = rfm9x.receive(timeout=5) # wait 5 seconds for reciever timeout
    print("Received")
    if packet is None: # idle RX mode
        print("Waiting for Packet")
    else: # If a packet is recieved, enter data  RX mode
        # try: # Try to recieve unless there is an error at any point in the rest of this try portion, ignore for now
        pkt_num_rec = ""
        while packet is not None: # Keep going as long as packets are recieved
            error = 0
            try:
                packet_text = str(packet, "utf-8") # get string from packet
                dest_addr = packet_text[1]
                pkt_num_rec = packet_text[3:5]
                routing_num = packet_text[0]
            except UnicodeDecodeError:
                print("An error has occured",)
                error = 1
            if error != 1:
                print("Full packet txt received:" + packet_text)
                if routing_num != "3" and routing_num != "4":
                    print("There has been a problem in sending, aborting to top function")
                    return
                if dest_addr == node_num:
                    packet_text = packet_text[header_size:] # get data from packet
                    if pkt_num_rec == pkt_number[2:]: # compare hex digits to the pkt_number
                        # Write data to file
                        print("Recieved Packet number: " + pkt_num_rec + " Writing to " + receivedfile + " now")
                        w.write(packet_text)
                        prev_pkt_num = pkt_number 
                        pkt_number = incPktNum(pkt_number)
                        next_pkt_request = routing_num + source_addr + node_num + pkt_number[2:] # increment packet number
                        print("next_pkt_req: " + next_pkt_request)
                        next_pkt_request = bytes(next_pkt_request,"utf-8") #convert next_pkt_request to bytes
                        print("Requesting Next Packet")
                        #time.sleep(1); # removed this sleep to make it faster, still sends large files when commented
                        rfm9x.send(next_pkt_request)
                        if routing_num == "4":
                            print("All packets received successfully, going back to main")
                            return
                    elif pkt_num_rec == prev_pkt_num[2:]:
                        rfm9x.send(next_pkt_request)
            packet = None
            packet = rfm9x.receive(timeout = 15)

######### Transmit Mode
def sendFile(pkt_rec, source_addr): # TX Mode
    currentfile = pkt_rec
    file_size = os.stat("tx_dir/" + currentfile).st_size # get file size in bytes
    f = open("tx_dir/" + currentfile, "r") # open file, changed to reading bytes cause sotemise its bigger

    # Skip sending if there are not enough bits
    max_num_of_packets = (16**header_size) # calc maximum number of packets than can be sent, a**b =a^b
    num_of_chunks = file_size/chunk_size
    max_file_size = max_num_of_packets * chunk_size
    file_too_big = packet_size_error = False # Errors for if the file is too big, and if packets are too big
    if (num_of_chunks > max_num_of_packets): # If the amount of packets exceeds pkt_num range
        file_too_big = True # do not send file by skipping the next while loop
    print("It will take at least " + str(num_of_chunks) + " packets to send " + currentfile)

    sent_size = 0 # Clear sent size before sending file
    pkt_num = "0x00" # start with packet 0 
    next_pkt_num = incPktNum(pkt_num)

    while sent_size < file_size and file_too_big == False:
        print("Getting Chunk, beginning packet sending shortly ")
        data = f.read(chunk_size) # read chunk of file for data
        routing_num = "3"
        if len(data) < chunk_size:
            routing_num = "4"
        header = routing_num + source_addr + node_num + pkt_num[2:] # get last characters from pkt-num
        tx_data = header + data # add header and data
        print("The full packet (tx_data) is: " + tx_data)
        tx_data = bytes(tx_data,"utf-8") # format data for packet

        # Send 1 packet and check for ACK, resend if necasary
        packet = None # Clear packet in order to check for one.
        tries = 0; # clear tries for next send
        if len(tx_data) > 252: # If a Unicode character is encountered, it might not fit into a byte
            packet_size_error = True
            break # stop trying to send this file
        rfm9x.send(tx_data)
        #packet = True # Uncomment to skip the following loop.
        while tries < 3 and packet is None: # try sending 3 times
            error = 0
            print("    Checking for ACK, pausing for 5 seconds")
            packet = rfm9x.receive(timeout = 5) # Wait for 5 seconds for receiever to request packet
            if packet is None: # If no packet received
                print("No ACK, Resending packet number " + pkt_num)
                rfm9x.send(tx_data) # send packet again
                tries += 1 # incement tries
            else: # IF a packet is received
                try:
                    packet_txt = str(packet,"utf-8") #convert packet to string, should have two characters
                except UnicodeDecodeError:
                    print("Decode error has occured")
                    error = 1
                if error != 1:
                    print("Ack Received")
                    dest_addr = packet_txt[1]
                    if dest_addr == node_num:
                        if packet_txt[3:] != next_pkt_num[2:]: # if the received packet is equal to packet_num
                            print("Error in received pkt, resending")
                            print("Correct: " + str(packet_txt) + " Other: " + str(next_pkt_num))
                            rfm9x.send(tx_data) # send packet gain
                            tries += 1
                            packet = None # empty packet to start try loop again
                    if dest_addr != node_num:
                        print("Received packet intended for other pi, continuing")
                        packet_txt = None
                    # go back to start of try sending 3 times unless the packet =/= pkt_num

        if tries >= 3: # If no ACK is recieved from reciever after 3 attempts
            print("No acknowledge recieved, canceling send")
            break # Exits  [while sent_size < file_size:] and leads to the restart of TX mode
        # At this point it is assumed that the paket was correctly sent and recieved

        # Increment pkt_num with string format for next packet
        print("pkt_num is currently " + pkt_num[2:]) # print last charaters
        pkt_num = incPktNum(pkt_num) # takes string, adds one, converts pack to string
        print("pkt_num is now " + pkt_num[2:] + "\n") # print last two characters (hex Digits) from pkt_n
        next_pkt_num = incPktNum(pkt_num)
        # Increase sent size (assume packet was sent for now)
        sent_size = sent_size + chunk_size # print("sent_size is now: " + str(sent_size)) 
        # Go back to     while sent_size < file_size:

    # At this Point, the file should be either sent or too many failed attempts to send it occured
    if (tries == 3):
        print("ERROR:, too many failed attepmts to send file, the file was not fully sent")
    elif file_too_big == True:
        print("ERROR: FILE TOO BIG! File size of " + str(file_size) + " exceeds "+ str(max_file_size) + " byte max")
    elif packet_size_error == True:
        print("ERROR: too many bytes, please reduce max_pkt_size to send this file or remove Unicode characters")
    else: # if no errors
        print(" FILE HAS FINISHED SENDING with NO ERRORS  *********************************************** ")
    print(    "__________END OF FILE SENDING___________________________") # better show the restart of TX mode
    time.sleep(1) # Pause for 1 second, go back to asking user for file to send
    #End of TX mode, go back to start of tx mode

while True:
    error = 0
    print("Sending file names")
    file_names = ""
    pkt_rec = None
    for x in range(len(files)):
        file_names += files[x] + "\n"
    file_names = bytes("0f" + node_num + "00" + file_names, "utf-8")
    rfm9x.send(file_names)
    pkt_rec = rfm9x.receive(timeout = random.randint(3,8))
    if pkt_rec is not None:
        try:
            pkt_rec = str(pkt_rec, "utf-8")
        except UnicodeDecodeError:
            error = 1
        if error != 1:
            routing_num = pkt_rec[0]
            print("routingnum:" + routing_num)
            dest_addr = pkt_rec[1]
            source_addr = pkt_rec[2]
            pkt_rec = pkt_rec[5:]
            if dest_addr == node_num or dest_addr == all_nodes:
                if routing_num == "0":
                    print("Files open for business:\n")
                    print(pkt_rec)
                    file_choice = ""
                    file_choice = input("Select a file, if no file wanted, push enter 'None'\n")
                    if file_choice != "None":
                        print("requesting file: " + file_choice)
                        request(file_choice, source_addr)
                elif routing_num == "1":
                    print("Pi #" + source_addr + "is requesting file: "+ pkt_rec)
                    sendFile(pkt_rec, source_addr)
                elif routing_num == "3":
                    print("Sleeping to break pi out of cycle")
                    time.sleep(25)


while True: # End Idle Mode (optional if a break in the TX mode
    print("An ERROR has occured, One of the modes has been exited please restart program")
    time.sleep(5)
