#!/usr/bin/env python
# coding: latin-1

# Import libary functions we need
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import time

# Set which GPIO pins the drive outputs are connected to
Output_1 = 4
Output_2 = 18
Output_3 = 8
Output_4 = 7

# Set all of the drive pins as output pins
GPIO.setup(Output_1, GPIO.OUT)
GPIO.setup(Output_2, GPIO.OUT)
GPIO.setup(Output_3, GPIO.OUT)
GPIO.setup(Output_4, GPIO.OUT)

# Map the on/off state to nicer names for display
dName = {}
dName[True] = 'ON '
dName[False] = 'OFF'

# Function to set all drives off
def MotorOff():
    GPIO.output(Output_1, GPIO.LOW)
    GPIO.output(Output_2, GPIO.LOW)
    GPIO.output(Output_3, GPIO.LOW)
    GPIO.output(Output_4, GPIO.LOW)

# Setup for processor monitor, adjust your temperature here. The fan will stay on between tempHigh and tempLow. 
# Default at 50 degrees celsius and 33 degrees celsius.
lProcessorFans = [Output_1]                              # List of fans to turn on when processor is too hot
pathSensor = '/sys/class/thermal/thermal_zone0/temp'    # File path used to read the temperature
readingPrintMultiplier = 0.001                          # Value to multiply the reading by for user display
# Add toggle for 'F
# x = y / 32 * 0.8 or something...
tempHigh = 50000                                        # Reading at which the fan(s) will be started (same units as file)
tempLow = 33000                                         # Reading at which the fan(s) will be stopped (same units as file)
# move timer to schedule try
interval = 5                                            # Time between readings in seconds

try:
    # Start by turning all drives off
    MotorOff()
    #raw_input('You can now turn on the power, press ENTER to continue')
    fansOn = False
    while True:
        # Read the temperature in from the file system
        fSensor = open(pathSensor, 'r')
        reading = float(fSensor.read())
        fSensor.close()
        # Adjust fan(s) depending on current status
        if fansOn:
            if reading <= tempLow:
                # We have cooled down enough, turn the fans off
                for fan in lProcessorFans:
                    GPIO.output(fan, GPIO.LOW)
                fansOn = False
        else:
            if reading >= tempHigh:
                # We have warmed up enough, turn the fans on
                for fan in lProcessorFans:
                    GPIO.output(fan, GPIO.HIGH)
                fansOn = True
        # Print the latest reading and the current state of all 4 drives
        print '%02.3f %s %s %s %s' % (reading * readingPrintMultiplier, dName[GPIO.input(DRIVE_1)], dName[GPIO.input(DRIVE_2)], dName[GPIO.input(DRIVE_3)], dName[GPIO.input(DRIVE_4)])
        # Wait a while
        time.sleep(interval)
except KeyboardInterrupt:
    # CTRL+C exit, turn off the drives and release the GPIO pins
    print 'Terminated'
    MotorOff()
    raw_input('Turn the power off now, press ENTER to continue')
    GPIO.cleanup()

