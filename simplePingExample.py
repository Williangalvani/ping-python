#!/usr/bin/python -u
#simplePingExample.py
from Ping import Ping
import sys
import getopt

device = ''
instructions = "Usage: python simplePingExample.py -d <device_name>"

##Parse Command line options
############################
try:
    options, remainder = getopt.getopt(sys.argv[1:],"hd:",["help", "device="])
except:
    print(instructions)
    exit(1)

for opt, arg in options:
    if opt in ('-h', '--help'):
        print(instructions)
        exit(1)
    elif opt in ('-d', '--device'):
        if (arg != ''):
            device = arg
    else:
        print(instructions)
        exit(1)

#Make a new Ping
myPing = Ping.Ping1D(device)
if myPing.initialize() is False:
    print "Failed to initialize Ping!"
    exit(1)

print("------------------------------------")
print("Starting Ping..")
print("Press CTRL+Z to exit")
print("------------------------------------")

raw_input("Press Enter to continue...")

# Read and print distance measurements with confidence
while True:
    myPing.getDistanceData()
    print("Distance: " + str(myPing.distance) + " Confidence: " + str(myPing.confidence))
