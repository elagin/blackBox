#!/usr/bin/python
import pynmea2

#http://aprs.gids.nl/nmea
#http://www.hydromaster.ru/gps/nmea.html
#https://github.com/Knio/pynmea2/blob/master/test/test_types.py

def getGPXHeader():
	xmlHeader = '<?xml version="1.0" encoding="UTF-8"?>'
	gpxHeader = '<gpx\r\n' + 'xmlns="http://www.topografix.com/GPX/1/1"\r\n' + 'version="1.1"\r\n' + 'creator="Wikipedia"\r\n' + 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\r\n' + 	'xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">\r\n'
	meta = '<time>2011-09-22T18:56:51Z</time> <metadata> <name>Name</name> <desc>Description</desc> <author> <name>Autor</name> </author> </metadata>'
	start = '<trk> <name>exercise</name>'
	end = '</trk> </gpx>'
	segStart = '<trkseg>'
	segEnd = '</trkseg>'
	
	res = xmlHeader + gpxHeader + meta + start + segStart
	print res
	exit()

def getGPXPoint(line):
	    #<trkpt lat="59.934721667" lon="30.310183333">
        #<time>2011-09-22T18:56:51Z</time>
        #<fix>2d</fix>
        #<sat>5</sat>
		#</trkpt>
	
	msg = pynmea2.parse(line)
	trkptStart = '<trkpt lat="' + str(msg.latitude) + '" lon="' + str(msg.longitude) + '">'
	trkptTime = '\r\n\t<time>2011-09-22T18:56:51Z</time>'
	trkptEnd = '\r\n</trkpt>'
	sats = '\r\n\t<sat>' + str(msg.num_sats) + '</sat>'
	ele = '\r\n\t<ele>' + str(msg.altitude) + '</ele>'
	
	res = trkptStart + trkptTime + sats + ele + trkptEnd
	return res

#f1 = open('180425-235321.csv', 'r') #open and read only
f1 = open('180427-041705.csv', 'r') #open and read only
try: #best to use try/finally so that the file opens and closes correctly
	#getGPXHeader()
	for line in f1: #read each line in temp.txt
		if line[:1] == '$':
			if '$GPGGA' in line and len(line) > 59:
				msg = pynmea2.parse(line)
				print getGPXPoint(line)
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