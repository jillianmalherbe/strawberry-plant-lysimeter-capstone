# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
from adafruit_seesaw.seesaw import Seesaw


class soilMoisture:
    #Can print the temperature and moisture
    
    # constructor for the soil moisture class
    def __init__(self):
        i2c_bus = board.I2C()  # uses board.SCL and board.SDA
        self.ss = Seesaw(i2c_bus, addr=0x36)

    # gets the moisture level through capacitive touch pad
    def get_moist(self):
        return self.ss.moisture_read()

    # gets the temperature in degrees C
    def get_temp(self):
        return self.ss.get_temp()
