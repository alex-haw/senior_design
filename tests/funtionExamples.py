# This function uses global variables to pass through a function
'''
import time
num = 2

def func1():
        return num*2

while True:
	print("Num is " + str(num))
	num = func1()
	print("Num*2 is" + str(num))
	time.sleep(2)
'''


# This function passes parameters
'''
import time

def func1(a):
	return a*2

while True:
	num = 2
	num = func1(num)
	print("Num is " + str(num))
	num = func1(num)
	print("Num is " + str(num))
	time.sleep(2)
'''


# This function shows how to do a void function
'''
import time
def printVoid():
	print("This is similar to a void function")

while True:
	printVoid()
	time.sleep(2)
'''
