import board
import adafruit_scd30

scd = adafruit_scd30.SCD30(board.I2C())

print("Data available?", scd.data_available)
print("CO2:", scd.CO2, "PPM")
print("Temperature:", scd.temperature, "degrees C")
print("Humidity:", scd.relative_humidity, "%%rH")
