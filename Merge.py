import serial
import pynmea2
import os
import time
from datetime import datetime
from mpu6050 import mpu6050
from bmp280 import BMP280
from smbus import SMBus

sensor = mpu6050(0x68)
bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus)

# clear previous data in data,txt
if os.path.exists("latdata.txt"):
	os.remove("latdata.txt")
if os.path.exists("lngdata.txt"):
	os.remove("lngdata.txt")
if os.path.exists("timedata.txt"):
	os.remove("timedata.txt")
#-
if os.path.exists("accx.txt"):
	os.remove("accx.txt")
if os.path.exists("accy.txt"):
	os.remove("accy.txt")
if os.path.exists("accz.txt"):
	os.remove("accz.txt")
if os.path.exists("gyrox.txt"):
	os.remove("gyrox.txt")
if os.path.exists("gyroy.txt"):
	os.remove("gyroy.txt")
if os.path.exists("gyroz.txt"):
	os.remove("gyroz.txt")
#-
if os.path.exists("temp.txt"):
	os.remove("temp.txt")
if os.path.exists("press.txt"):
	os.remove("press.txt")
if os.path.exists("alt.txt"):
	os.remove("alt.txt")


file1 = open('latdata.txt','w')
file2 = open('lngdata.txt','w')
file3 = open('timedata.txt','w')
#-
file4 = open('accx.txt','w')
file5 = open('accy.txt','w')
file6 = open('accz.txt','w')
file7 = open('gyrox.txt','w')
file8 = open('gyroy.txt','w')
file9 = open('gyroz.txt','w')
#-
file10 = open('temp.txt','w')
file11 = open('press.txt','w')
file12 = open('alt.txt','w')

data_count = 0

while True:
	# get current time
	current_time = datetime.now()
	# turn current_time into string 
	formatted_time = current_time.strftime("%Y.%m.%d_%H:%M:%S")
	
	print(formatted_time)
		
	file3.write(str(formatted_time))
	file3.write("\n")
	
	
	port="/dev/ttyAMA0"
	ser=serial.Serial(port, baudrate=9600, timeout=0.5)
	dataout = pynmea2.NMEAStreamReader()
	newdata=ser.readline()
	n_data=newdata.decode("latin-1")
	if n_data[0:6] == "$GPRMC":
		newmsg=pynmea2.parse(n_data)
		lat=newmsg.latitude
		lng=newmsg.longitude
		lat1=round(lat,4)
		lng1=round(lng,4)
	
		file1.write(str(lat1))
		file1.write("\n") #change row
		file2.write(str(lng1))
		file2.write('\n')
		
		gps = "Lat = "+str(lat1)+", Lng = "+str(lng1)+" "
		print(gps)

	
	accel_data = sensor.get_accel_data()
	gyro_data = sensor.get_gyro_data()
	
	file4.write(str(accel_data['x']))
	file4.write("\n")
	file5.write(str(accel_data['y']))
	file5.write("\n")
	file6.write(str(accel_data['z']))
	file6.write("\n")
	file7.write(str(gyro_data['x']-47))
	file7.write("\n")
	file8.write(str(gyro_data['y']))
	file8.write("\n")
	file9.write(str(gyro_data['z']))
	file9.write("\n")	
	
	temperature = bmp280.get_temperature()
	pressure = bmp280.get_pressure()
	altitude = bmp280.get_altitude()
	format_temp = "{:05.2f}".format(temperature)
	format_pressure = "{:05.2f}".format(pressure)
	format_altitude = "{:05.2f}".format(altitude)
	
	file10.write(str(format_temp))
	file10.write("\n")
	file11.write(str(format_pressure))
	file11.write("\n")
	file12.write(str(format_altitude))
	file12.write("\n")
	
	data_count +=1
	
	mpu6050.a = 'x:'+ str(accel_data['x'])+' y:'+ str(accel_data['y']) + 'z:'+ str(accel_data['z'])
	mpu6050.g = 'x:'+ str(gyro_data['x']-47)+' y:'+ str(gyro_data['y'])+' z:'+ str(gyro_data['z'])
	bmp = str(format_temp)+" "+str(format_pressure)+" "+str(format_altitude)

	print(mpu6050.a+"\n"+mpu6050.g)
	print(bmp)
	
	if data_count ==5:
		file1.flush()
		file2.flush()
		file3.flush()
		file4.flush()
		file5.flush()
		file6.flush()
		file7.flush()
		file8.flush()
		file9.flush()
		file10.flush()
		file11.flush()
		file12.flush()
		
		os.fsync(file1.fileno())
		os.fsync(file2.fileno())
		os.fsync(file3.fileno())
		os.fsync(file4.fileno())
		os.fsync(file5.fileno())
		os.fsync(file6.fileno())
		os.fsync(file7.fileno())
		os.fsync(file8.fileno())
		os.fsync(file9.fileno())
		os.fsync(file10.fileno())
		os.fsync(file11.fileno())
		os.fsync(file12.fileno())
		data_count = 0
	time.sleep(1)


				

file1.close()
file2.close()
file3.close()
file4.close()
file5.close()
file6.close()
file7.close()
file8.close()
file9.close()
file10.close()
file11.close()
file12.close()
