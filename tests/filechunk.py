# This file breaks up files into chunks so that large files can be sent as packets

import time
import os

files = os.listdir('tx_dir/')
currentfile = files[0]
i = 0
chunk_size = 10 # chunk size in bytes

while True:
	# Show Files
	print("** The current files in transmit_directory/ are:")
	for x in range(len(files)):
		print(files[x])
	
	# Prompt for user to select file
	print("What file would you like to open?")
	currentfile = input()

	# Show file info
	currentfilesize = os.stat("tx_dir/" + currentfile).st_size
	print("The size of " +currentfile + " is: " + str(currentfilesize) + " bytes")
	
	# Open file
	f = open("tx_dir/" + currentfile, "r")
	
	# Break file into chunks
	chunk1 = f.read(chunk_size) # first chunk_size of file
	chunk2 = f.read(chunk_size) # second chunk_size of file
	chunk3 = f.read(chunk_size)
	# Show Chunks
	print("The first " + str(chunk_size) + " byte chunk of " + currentfile + " is:" + str(chunk1))
	print("The second " + str(chunk_size) + " byte chunk of " + currentfile + " is:" + str(chunk2))
	print("The third " + str(chunk_size) + " byte chunk of " + currentfile + " is:" + str(chunk3))

	#print("The contents of " + currentfile +" is:\n")
	#f = open("tx_dir/" + currentfile, "r")
	#for line in f:
	#	print(line)	
	#start = f.read(1)
	#print(start)
	time.sleep(5) # i'm going to pause for 5 seconds
