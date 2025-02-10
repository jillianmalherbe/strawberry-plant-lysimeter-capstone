import smbus2
import time

# I2C address for MLX90614
MLX90614_I2C_ADDR = 0x5A

# Register addresses for reading ambient and object temperatures
AMBIENT_TEMP_REG = 0x06
OBJECT_TEMP_REG = 0x07

# SMBus setup
bus = smbus2.SMBus(1)  # Use "1" for Raspberry Pi's I2C bus


def read_temperature(register):
    # Read two bytes from the given register
    data = bus.read_word_data(MLX90614_I2C_ADDR, register)

    # Convert the data to a temperature in Celsius
    temp = (data * 0.02) - 273.15
    return temp


try:
    while True:
        ambient_temp = read_temperature(AMBIENT_TEMP_REG)
        object_temp = read_temperature(OBJECT_TEMP_REG)

        print(f"Ambient Temperature: {ambient_temp:.2f} °C")
        print(f"Object Temperature: {object_temp:.2f} °C")

        time.sleep(1)

except KeyboardInterrupt:
    print("Temperature reading stopped by user.")

finally:
    bus.close()
