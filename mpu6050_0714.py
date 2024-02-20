from mpu6050 import mpu6050
import time
import os
from datetime import datetime

sensor = mpu6050(0x68)

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
if os.path.exists("m_timedata.txt"):
	os.remove("m_timedata.txt")
	
file1 = open('accx.txt','w')
file2 = open('accy.txt','w')
file3 = open('accz.txt','w')
file4 = open('gyrox.txt','w')
file5 = open('gyroy.txt','w')
file6 = open('gyroz.txt','w')
file7 = open('m_timedata','w')

data_count = 0

while True:
	# get current time
	current_time = datetime.now()
	# turn current_time into string 
	milliseconds = current_time.microsecond // 1000
	formatted_time = current_time.strftime("%Y.%m.%d_%H:%M:%S") + ".{:03d}".format(milliseconds)	
	file7.write(str(formatted_time))
	file7.write('\n')
	
	accel_data = sensor.get_accel_data()
	print('Accelermeter')
	print('x:'+ str(accel_data['x']))
	print('y:'+ str(accel_data['y']))
	print('z:'+ str(accel_data['z']))
	
	file1.write(str(accel_data['x']))
	file1.write("\n")
	file2.write(str(accel_data['y']))
	file2.write("\n")
	file3.write(str(accel_data['z']))
	file3.write("\n")
	
	gyro_data = sensor.get_gyro_data()
	print('Gyro')
	print('x:'+ str(gyro_data['x']-47))
	print('y:'+ str(gyro_data['y']))
	print('z:'+ str(gyro_data['z']))
	file4.write(str(gyro_data['x']-47))
	file4.write("\n")
	file5.write(str(gyro_data['y']))
	file5.write("\n")
	file6.write(str(gyro_data['z']))
	file6.write("\n")
	
	data_count +=1	
		
	if data_count ==3:
		file1.flush()
		file2.flush()
		file3.flush()
		file4.flush()
		file5.flush()
		file6.flush()
		file7.flush()
		os.fsync(file1.fileno())
		os.fsync(file2.fileno())
		os.fsync(file3.fileno())
		os.fsync(file4.fileno())
		os.fsync(file5.fileno())
		os.fsync(file6.fileno())
		os.fsync(file7.fileno())
		data_count = 0
		
	time.sleep(0.2)

file1.close()
file2.close()
file3.close()
file4.close()
file5.close()
file6.close()
file7.close()
