"""
This Raspberry Pi code was developed by newbiely.com
This Raspberry Pi code is made available for public use without any restriction
For comprehensive instructions and wiring diagrams, please visit:
https://newbiely.com/tutorials/raspberry-pi/raspberry-pi-water-liquid-valve
"""


import RPi.GPIO as GPIO
import time

# Set the GPIO mode (BCM or BOARD)
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin controls the water valve via the relay module
RELAY_PIN = 12

# Set the relay pin as an output pin
GPIO.setup(RELAY_PIN, GPIO.OUT)

try:
    # Run the loop function indefinitely
    while True:
        # Turn the relay ON (HIGH) to turn on the water valve
        GPIO.output(RELAY_PIN, GPIO.HIGH)
        time.sleep(20)  # Wait for 5 seconds

        # Turn the relay OFF (LOW) to turn off the water valve
        GPIO.output(RELAY_PIN, GPIO.LOW)
        time.sleep(20)  # Wait for 5 seconds

except KeyboardInterrupt:
    # If the user presses Ctrl+C, clean up the GPIO configuration
    GPIO.cleanup()
