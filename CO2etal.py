import board
import adafruit_scd30

class CO2:
	#Can print the c02 levels, temperature, and humidity
	
	# constructor for the co2 class
	def __init__(self):
		self.scd = adafruit_scd30.SCD30(board.I2C())
		print(self.scd)

	# gets if the data is available to read
	def get_data_available(self):
		return self.scd.data_available

	# gets the co2 in ppm
	def get_co2(self):
		return self.scd.CO2

	# gets the temperature in degrees C
	def get_temp(self):
		return self.scd.temperature

	# gets the humidity in rH
	def get_humid(self):
		return self.scd.relative_humidity
     
