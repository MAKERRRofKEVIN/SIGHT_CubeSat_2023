import time
import os
from bmp280 import BMP280
from smbus import SMBus

bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus)
if os.path.exists("temp.txt"):
	os.remove("temp.txt")
if os.path.exists("press.txt"):
	os.remove("press.txt")
if os.path.exists("alt.txt"):
	os.remove("alt.txt")

file1 = open('temp.txt','w')
file2 = open('press.txt','w')
file3 = open('alt.txt','w')

data_count = 0

while True:
		
	temperature = bmp280.get_temperature()
	pressure = bmp280.get_pressure()
	altitude = bmp280.get_altitude()
	format_temp = "{:05.2f}".format(temperature)
	format_pressure = "{:05.2f}".format(pressure)
	format_altitude = "{:05.2f}".format(altitude)
	
	file1.write(str(format_temp))
	file1.write("\n")
	file2.write(str(format_pressure))
	file2.write("\n")
	file3.write(str(format_altitude))
	file3.write("\n")
	
	data_count +=1
		
	if data_count ==5:
		file1.flush()
		file2.flush()
		file3.flush()
		os.fsync(file1.fileno())
		os.fsync(file1.fileno())
		os.fsync(file1.fileno())
		data_count = 0
			
	print(format_temp + "  " + format_pressure + "  " + format_altitude)
	time.sleep(1)

file1.close()
file2.close()
file3.close()
