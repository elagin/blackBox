#!/usr/bin/python

from pynmea import nmea
#import matplotlib.pyplot as plt
import serial, time, sys, threading, datetime, shutil
import string
from pynmea.streamer import NMEAStream

global alt, i

f1 = open('180427-041705-new.csv', 'r') #open and read only
try: #best to use try/finally so that the file opens and closes correctly
	gpgga = nmea.GPGGA()
	for line in f1: #read each line in temp.txt
		if '$GPGGA' in line and len(line) > 59:
			print line
			gpgga.parse(line)
			#print line + " - " + str(len(line))
			
			lats = gpgga.latitude
			print "Latitude values : " + str(lats)

			lat_dir = gpgga.lat_direction
			print "Latitude direction : " + str(lat_dir)

			longitude = gpgga.longitude
			print "Longitude values : " + str(longitude)

			long_dir = gpgga.lon_direction
			print "Longitude direction : " + str(long_dir)

			time_stamp = gpgga.timestamp
			print "GPS time stamp : " + str(time_stamp)

			alt = gpgga.antenna_altitude
			print "Antenna altitude : " + str(alt)

			lat_deg = lats[0:2]
			lat_mins = lats[2:4]
			if len(lats) > 0:
				lat_secs = round(float(lats[5:])*60/10000, 2)

			latitude_string = lat_deg + u'\N{DEGREE SIGN}' + lat_mins + string.printable[68] + str(lat_secs) + string.printable[63]
			print latitude_string

			lon_deg = longitude[0:3]
			lon_mins = longitude[3:5]
			if len(longitude) > 0:
				lon_secs = round(float(longitude[6:])*60/10000, 2)
			lon_str = lon_deg + u'\N{DEGREE SIGN}' + lon_mins + string.printable[68] + str(lon_secs) + string.printable[63]
			#print "Longitude : " + str(lon_str)
			print "=================="
		#else if 'GPRMC' in line:
		#	gpprmc = nmea.GPRMC()
		#	gpprmc.parse(line)

						#plt.scatter(x=[i], y=[float(alt)], s = 1, c='r') #plot each point
						
finally:
    f1.close()
