import CO2etal as co2
import soilMoisture as moist
import leafIR as ir
import pressure as pres
import loadCell as load

# for the load cell
load_cell = load.loadCell()
load_cell.calibrate()
print("Item weighs {} grams.\n".format(load_cell.get_mass()))
print("\nOffset: {}\nScale: {}".format(load_cell.get_offset(), load_cell.get_scale()))       


# for the co2 sensor
# create a co2 class
co2_sensor = co2.CO2()

# print the c02 data
print("Data available?", co2_sensor.get_data_available())
print("CO2:", co2_sensor.get_co2(), "PPM")
print("Temperature:", co2_sensor.get_temp(), "degrees C")
print("Humidity:", co2_sensor.get_humid(), "%%rH")


# for the soil moisture sensor
moist_sensor = moist.soilMoisture()
print("temp: " + str(moist_sensor.get_temp()))
print("moisture: " + str(moist_sensor.get_moist()))

# Read data for pressure sensor
pres_sensor = pres.Pressure()
bmp_temp, pressure = pres_sensor.get_temp_and_pressure()

# Print results
print(f"Temperature: {bmp_temp:.2f}°C, Pressure: {pressure:.2f} Pa")

# Read data for leaf ir sensor
ir_sensor = ir.leafIR()
ambient_temp = ir_sensor.get_ambient_temp()
object_temp = ir_sensor.get_object_temp()

print(f"Ambient Temperature: {ambient_temp:.2f} °C")
print(f"Object Temperature: {object_temp:.2f} °C")

print("Item weighs {} grams.\n".format(load_cell.get_mass()))
print("\nOffset: {}\nScale: {}".format(load_cell.get_offset(), load_cell.get_scale()))  
'''
#finish this at the end!!
#ir_sensor.final()
'''

