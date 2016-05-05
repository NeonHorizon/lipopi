#!/usr/bin/env python

# lipopi.py

# Example python script that uses the LiPoPi circuitry to handle the safe shutdown of
# a Raspberry Pi in response to user request or low battery

# See the README file for details on how to set this up with systemd

# this script is called by /etc/systemd/system/lipopi.service

# This version uses the GPIO event trigger machinery

# 2016 - Robert Jones - Freely distributed under the MIT license

# based on Daniel Bull's LiPoPi project - https://github.com/NeonHorizon/lipopi

import os
import RPi.GPIO as GPIO
import time

# Configure the GPIO pins

def lipopi_setup():
    global lipopi
    
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # setup the pin to check the shutdown switch - use the internal pull down resistor
    GPIO.setup(lipopi['shutdown_pin'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # setup the low battery check pin
    GPIO.setup(lipopi['low_battery_pin'], GPIO.IN)

    # create a trigger for the shutdown switch and low battery pins

    GPIO.add_event_detect(lipopi['shutdown_pin'], GPIO.RISING, callback=lipopi_user_shutdown, bouncetime=300)

    GPIO.add_event_detect(lipopi['low_battery_pin'], GPIO.FALLING, callback=lipopi_low_battery_shutdown, bouncetime=300)

    # open log file in append mode
    lipopi['logfile_pointer'] = open(lipopi['logfile'], 'a+')  


# Detect when the switch is pressed - wait shutdown_wait seconds - then shutdown

def lipopi_user_shutdown(channel):
    global lipopi

    cmd = "sudo wall 'System shutting down in %d seconds'" % lipopi['shutdown_wait']
    os.system(cmd)
    
    time.sleep(lipopi['shutdown_wait'])

    msg = time.strftime("User Request - Shutting down at %a, %d %b %Y %H:%M:%S +0000\n", time.gmtime())
    lipopi['logfile_pointer'].write(msg)
    lipopi['logfile_pointer'].close()
    GPIO.cleanup()
    os.system("sudo shutdown now")


# Respond to a low battery signal from the PowerBoost and shutdown
# Pin goes low on low battery 

def lipopi_low_battery_shutdown(channel):
    global lipopi

    cmd = "sudo wall 'System shutting down in %d seconds'" % lipopi['shutdown_wait']
    os.system(cmd)

    time.sleep(lipopi['shutdown_wait'])

    msg = time.strftime("Low Battery - Shutting down at %a, %d %b %Y %H:%M:%S +0000\n", time.gmtime())
    lipopi['logfile_pointer'].write(msg)
    lipopi['logfile_pointer'].close()
    GPIO.cleanup()
    os.system("sudo shutdown now")

# Close the log file, reset the GPIO pins
def lipopi_cleanup():
    global lipopi
    lipopi['logfile_pointer'].close()
    GPIO.cleanup()



# Main --------------------------------------------


# Setup LiPoPi global variable array

lipopi = {}

# Specify which GPIO pins to use
lipopi['low_battery_pin'] = 15

#lipopi['shutdown_pin']    = 18
lipopi['shutdown_pin']    = 21

lipopi['logfile'] = '/home/pi/lipopi.log'  # FULL path to the log file
# or do this relative to the location of this script?

lipopi['shutdown_wait'] = 2  # seconds - how long to wait before actual shutdown - can be 0 if you want

# setup the GPIO pins and event triggers

lipopi_setup()

# Although the shutdown is triggered by an interrupt, we still need a loop
# to keep the script from exiting - just do a very long sleep

while True:    
    time.sleep(6000)

# clean up if the script exits without machine shutdown

lipopi_cleanup()



        

