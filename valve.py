"""
This Raspberry Pi code was developed by newbiely.com
This Raspberry Pi code is made available for public use without any restriction
For comprehensive instructions and wiring diagrams, please visit:
https://newbiely.com/tutorials/raspberry-pi/raspberry-pi-water-liquid-valve
"""


import RPi.GPIO as GPIO
import time

class Valve:
    #Can turn the valve on and off
    valve_on=False
    
    # constructor
    def __init__(self):
        # Set the GPIO mode (BCM or BOARD)
        GPIO.setmode(GPIO.BCM)
        # Define the GPIO pin controls the water valve via the relay module
        self.RELAY_PIN = 12
        # Set the relay pin as an output pin
        GPIO.setup(self.RELAY_PIN, GPIO.OUT)

    def turn_off(self):
        # Turn the relay ON (HIGH) to turn on the water valve
        GPIO.output(self.RELAY_PIN, GPIO.HIGH)
        self.valve_on=False
    
    def turn_on(self):
        # Turn the relay OFF (LOW) to turn off the water valve
        GPIO.output(self.RELAY_PIN, GPIO.LOW)
        self.valve_on=True
        
    def is_on(self):
        return self.valve_on

