import time
import os

files = os.listdir('transmit_directory/')
currentfile = files[0]
i = 0

while True:
	print("** The current files in transmit_directory/ are:")
	for x in range(len(files)):
		print(files[x])
	print("What file would you like to open?")
	currentfile = input()
	f = open("transmit_directory/" + currentfile, "r")
	for line in f:
		print(line)
	time.sleep(5)
