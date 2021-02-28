import time
import os

files = os.listdir('tx_dir/')
currentfile = files[0]
i = 0

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
	start = f.read()
	print(start)
	time.sleep(5)
