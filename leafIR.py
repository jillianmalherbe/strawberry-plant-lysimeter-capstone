import smbus2
import time

class leafIR:
    #Can print the temperature of the object and ambient
    
    # constructor for the pressure class
    def __init__(self):
        # I2C address for MLX90614
        self.MLX90614_I2C_ADDR = 0x5A
        # Register addresses for reading ambient and object temperatures
        self.AMBIENT_TEMP_REG = 0x06
        self.OBJECT_TEMP_REG = 0x07
        # SMBus setup
        self.bus = smbus2.SMBus(1)  # Use "1" for Raspberry Pi's I2C bus

    def read_temperature(self, register):
        # Read two bytes from the given register
        data = self.bus.read_word_data(self.MLX90614_I2C_ADDR, register)

        # Convert the data to a temperature in Celsius
        temp = (data * 0.02) - 273.15
        return temp
        
    # gets the ambient temperature
    def get_ambient_temp(self):
        return self.read_temperature(self.AMBIENT_TEMP_REG)
    # gets the object temperature
    def get_object_temp(self):
        return self.read_temperature(self.OBJECT_TEMP_REG)
    
    def final(self):
        self.bus.close()
        
