#!/usr/bin/env python

import RPi.GPIO as GPIO
import subprocess
import time

subprocess.call(['python3','/home/pi/senior_design/finalizing/orange.py'])
time.sleep(.5)

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.wait_for_edge(4, GPIO.FALLING)

subprocess.call(['python3','/home/pi/senior_design/finalizing/bye.py'])
time.sleep(.5)

subprocess.call(['shutdown', '-h', 'now'], shell=False)
