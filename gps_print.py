import serial
import pynmea2
import os
import time
from datetime import datetime
# clear previous data in data,txt
if os.path.exists("latdata.txt"):
	os.remove("latdata.txt")
if os.path.exists("lngdata.txt"):
	os.remove("lngdata.txt")
if os.path.exists("timedata.txt"):
	os.remove("timedata.txt")
file1 = open('latdata.txt','w')
file2 = open('lngdata.txt','w')
file3 = open('timedata.txt','w')
while True:
	port="/dev/ttyAMA0"
	ser=serial.Serial(port, baudrate=9600, timeout=0.5)
	dataout = pynmea2.NMEAStreamReader()
	newdata=ser.readline()
	n_data=newdata.decode("latin-1")	
	# get current time
	current_time = datetime.now()
	# turn current_time into string 
	formatted_time = current_time.strftime("%Y.%m.%d_%H:%M:%S")
	if n_data[0:6] == "$GPRMC":
		newmsg=pynmea2.parse(n_data)
		lat=newmsg.latitude
		lng=newmsg.longitude
		lat1=round(lat,4)
		lng1=round(lng,4)
		gps = "Latitude="+str(lat1)+", Longitude="+str(lng1)+", Time="+formatted_time
		print(gps)
		file1.write(str(lat1))
		file1.write("\n") #change row
		file2.write(str(lng1))
		file2.write('\n')
		file3.write(str(formatted_time))
		file3.write("\n")	
file1.close()
file2.close()
file3.close()
