import smbus2
import time

class Pressure:
    #Can print the temperature and pressure
    
    # constructor for the pressure class
    def __init__(self):
        # I2C addresses for BMP280 and SHT40
        self.BMP280_I2C_ADDR = 0x76  # Default address for BMP280
        self.bus = smbus2.SMBus(1)  # Use 1 for Raspberry Pi I2C bus
        
    # gets the temperature and pressure
    def get_temp_and_pressure(self):
        # Configuration registers (oversampling, mode)
        self.bus.write_byte_data(self.BMP280_I2C_ADDR, 0xF4, 0x27)  # Normal mode, temp/pressure oversampling x1
        self.bus.write_byte_data(self.BMP280_I2C_ADDR, 0xF5, 0xA0)  # Config register, 1000ms standby time

        # Read raw temperature and pressure data (20 bits each)
        data = self.bus.read_i2c_block_data(self.BMP280_I2C_ADDR, 0xF7, 8)
        adc_p = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        adc_t = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)

        # Compensation parameters (from calibration registers)
        dig_T1 = self.bus.read_word_data(self.BMP280_I2C_ADDR, 0x88)
        dig_T2 = self.bus.read_word_data(self.BMP280_I2C_ADDR, 0x8A)
        dig_T3 = self.bus.read_word_data(self.BMP280_I2C_ADDR, 0x8C)
        dig_P1 = self.bus.read_word_data(self.BMP280_I2C_ADDR, 0x8E)
        dig_P2 = self.bus.read_word_data(self.BMP280_I2C_ADDR, 0x90)
        dig_P3 = self.bus.read_word_data(self.BMP280_I2C_ADDR, 0x92)
        dig_P4 = self.bus.read_word_data(self.BMP280_I2C_ADDR, 0x94)
        dig_P5 = self.bus.read_word_data(self.BMP280_I2C_ADDR, 0x96)
        dig_P6 = self.bus.read_word_data(self.BMP280_I2C_ADDR, 0x98)
        dig_P7 = self.bus.read_word_data(self.BMP280_I2C_ADDR, 0x9A)
        dig_P8 = self.bus.read_word_data(self.BMP280_I2C_ADDR, 0x9C)
        dig_P9 = self.bus.read_word_data(self.BMP280_I2C_ADDR, 0x9E)

        # Convert temperature
        var1 = ((((adc_t >> 3) - (dig_T1 << 1))) * dig_T2) >> 11
        var2 = (((((adc_t >> 4) - dig_T1) * ((adc_t >> 4) - dig_T1)) >> 12) * dig_T3) >> 14
        t_fine = var1 + var2
        temperature = (t_fine * 5 + 128) >> 8

        # Convert pressure
        var1 = t_fine - 128000
        var2 = var1 * var1 * dig_P6
        var2 = var2 + ((var1 * dig_P5) << 17)
        var2 = var2 + (dig_P4 << 35)
        var1 = ((var1 * var1 * dig_P3) >> 8) + ((var1 * dig_P2) << 12)
        var1 = (((1 << 47) + var1) * dig_P1) >> 33
        if var1 == 0:
            pressure = 0
        else:
            p = 1048576 - adc_p
            p = (((p << 31) - var2) * 3125) // var1
            var1 = (dig_P9 * (p >> 13) * (p >> 13)) >> 25
            var2 = (dig_P8 * p) >> 19
            pressure = ((p + var1 + var2) >> 8) + (dig_P7 << 4)
            
        return temperature / 100.0, pressure / 256.0

    def final(self):
        self.bus.close()
        
