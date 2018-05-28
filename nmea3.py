#!/usr/bin/python
import pynmea2

#http://aprs.gids.nl/nmea
#http://www.hydromaster.ru/gps/nmea.html

f1 = open('180425-235321.csv', 'r') #open and read only
try: #best to use try/finally so that the file opens and closes correctly
	for line in f1: #read each line in temp.txt
		if '$GPGGA' in line and len(line) > 59:
			msg = pynmea2.parse(line)
			#print '$GPGGA'
			print msg.timestamp
			#print "=================="
			continue
		elif '$GPRMC' in line and len(line) > 59:
			msg = pynmea2.parse(line)
			#print '$GPRMC'
			print msg.timestamp
			#print "=================="
			continue
		elif '$GPGLL' in line:
			#print line
			msg = pynmea2.parse(line)
			print msg.timestamp
			continue
		elif 'BB' in line:
			continue
		elif 'GPVTG' in line: #Track Made Good and Ground Speed. 
			#print line
			continue
		elif 'GPGSV' in line: #GPS Satellites in View
			#print line
			continue
		elif 'GPGSA' in line: #GPS DOP and active satellites 
			#print line
			continue
		elif 'GPTXT' in line:
			#print line
			continue
		elif 'GPRMC' in line: #Recommended minimum specific GPS/Transit data 
			#print line
			msg = pynmea2.parse(line)
			#print '$GPRMC'
			print msg.timestamp			
			continue
		else:
			#print line
			continue
finally:
    f1.close()