import time
import os

files = os.listdir('tx_dir/')
currentfile = files[0]
i = 0
chunksize = 1 # read file 1 byte at a time
charError = False

while True:
	print("** The current files in transmit_directory/ are:")
	for x in range(len(files)):
		print(files[x])
	print("What file would you like to open?")
	currentfile = input()
	currentfilesize = os.stat("tx_dir/" + currentfile).st_size
	print("The size of " +currentfile + " is: " + str(currentfilesize) + " bytes")
	#print("The contents of " + currentfile +" is:\n")
	f = open("tx_dir/" + currentfile, "r")
	#for line in f:
	#	print(line)	
	#start = f.read()
	#print(start)
	print("The file will now be printed one byte at a time until a problem char is found")
	i = 0
	while not charError:
		chunk = f.read(chunksize) 	
		chunk_bytes = bytes(chunk,"utf-8") # encode chunk (string) as bytes
		print("Chunk " + str(i) + " is: " + chunk)
		if len(chunk_bytes) > chunksize:
			charError = True
		else:
			i += 1
	print("Error: Prpoblem Char found at location: " + str(i))
	print("chunk is: " + chunk)
	print("chunk_bytes is: " + str(chunk_bytes))
	time.sleep(5)
