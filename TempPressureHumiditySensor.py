import smbus2
import time

# I2C addresses for BMP280 and SHT40
BMP280_I2C_ADDR = 0x76  # Default address for BMP280
SHT40_I2C_ADDR = 0x44  # Default address for SHT40

# I2C bus
bus = smbus2.SMBus(1)  # Use 1 for Raspberry Pi I2C bus


# BMP280 Functions
def read_bmp280_temp_and_pressure():
    # Configuration registers (oversampling, mode)
    bus.write_byte_data(BMP280_I2C_ADDR, 0xF4, 0x27)  # Normal mode, temp/pressure oversampling x1
    bus.write_byte_data(BMP280_I2C_ADDR, 0xF5, 0xA0)  # Config register, 1000ms standby time

    # Read raw temperature and pressure data (20 bits each)
    data = bus.read_i2c_block_data(BMP280_I2C_ADDR, 0xF7, 8)
    adc_p = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
    adc_t = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)

    # Compensation parameters (from calibration registers)
    dig_T1 = bus.read_word_data(BMP280_I2C_ADDR, 0x88)
    dig_T2 = bus.read_word_data(BMP280_I2C_ADDR, 0x8A)
    dig_T3 = bus.read_word_data(BMP280_I2C_ADDR, 0x8C)
    dig_P1 = bus.read_word_data(BMP280_I2C_ADDR, 0x8E)
    dig_P2 = bus.read_word_data(BMP280_I2C_ADDR, 0x90)
    dig_P3 = bus.read_word_data(BMP280_I2C_ADDR, 0x92)
    dig_P4 = bus.read_word_data(BMP280_I2C_ADDR, 0x94)
    dig_P5 = bus.read_word_data(BMP280_I2C_ADDR, 0x96)
    dig_P6 = bus.read_word_data(BMP280_I2C_ADDR, 0x98)
    dig_P7 = bus.read_word_data(BMP280_I2C_ADDR, 0x9A)
    dig_P8 = bus.read_word_data(BMP280_I2C_ADDR, 0x9C)
    dig_P9 = bus.read_word_data(BMP280_I2C_ADDR, 0x9E)

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


# SHT40 Functions
def read_sht40_temp_and_humidity():
    # Send measurement command (high repeatability)
    bus.write_i2c_block_data(SHT40_I2C_ADDR, 0xFD, [])
    time.sleep(0.01)  # Wait for measurement

    # Read 6 bytes of data
    data = bus.read_i2c_block_data(SHT40_I2C_ADDR, 0x00, 6)

    # Convert temperature
    temp_raw = (data[0] << 8) | data[1]
    temperature = -45 + (175 * (temp_raw / 65535.0))

    # Convert humidity
    hum_raw = (data[3] << 8) | data[4]
    humidity = 100 * (hum_raw / 65535.0)

    return temperature, humidity


# Main loop
try:
    while True:
        # Read data from BMP280
        bmp_temp, pressure = read_bmp280_temp_and_pressure()

        # Read data from SHT40
        sht_temp, humidity = read_sht40_temp_and_humidity()

        # Print results
        print(f"BMP280 -> Temperature: {bmp_temp:.2f}°C, Pressure: {pressure:.2f} Pa")
        print(f"SHT40 -> Temperature: {sht_temp:.2f}°C, Humidity: {humidity:.2f}%")
        print("-" * 40)

        time.sleep(1)  # Delay between readings

except KeyboardInterrupt:
    print("Exiting program...")
    bus.close()
