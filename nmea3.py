#!/usr/bin/python
import pynmea2

#http://aprs.gids.nl/nmea
#http://www.hydromaster.ru/gps/nmea.html
#https://github.com/Knio/pynmea2/blob/master/test/test_types.py

global datestampGlobal

def getGPXHeader():
	xmlHeader = '<?xml version="1.0" encoding="UTF-8"?>'
	gpxHeader = '<gpx\r' + 'xmlns="http://www.topografix.com/GPX/1/1"\r' + 'version="1.1"\r' + 'creator="Wikipedia"\r' + 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\r' + 	'xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">\r'
	meta = '<time>2011-09-22T18:56:51Z</time>\r<metadata>\r\t<name>Name</name>\r\t<desc>Description</desc>\r\t<author>\r\t\t<name>Autor</name>\r\t</author>\r</metadata>'
	start = '<trk> <name>exercise</name>'
	end = '</trk> </gpx>'
	segStart = '<trkseg>'
	return xmlHeader + gpxHeader + meta + start + segStart 
	
def getGPXEnder():
	segEnd = '</trkseg>\r</trk>\r</gpx>'
	return segEnd

def getGPXPoint(line):
	#print 'getGPXPoint'
	msg = pynmea2.parse(line)
	try:
		time = getTime(msg)
		if msg.latitude > 0 or msg.longitude > 0:
			#if 'writeName' in globals():
			trkptStart = '\r\t<trkpt lat="' + str(msg.latitude) + '" lon="' + str(msg.longitude) + '">'
			#trkptTime = '\r\t<time>2011-09-22T18:56:51Z</time>'
			#trkptTime = getTime(msg)
			trkptEnd = '\r</trkpt>'
			res = trkptStart + time
			if hasattr(msg, 'num_sats'):
				sats = '\r\t<sat>' + str(msg.num_sats) + '</sat>'
				res = res + sats
			if hasattr(msg, 'altitude'):
				ele = '\r\t<ele>' + str(msg.altitude) + '</ele>'
				res = res + ele
			#ele = '\r\t<ele>' + str(msg.altitude) + '</ele>'
			#res = res + sats
			#res = res + ele
			res = res + trkptEnd
			#+ sats + ele + trkptEnd
			return str(res)
	except AttributeError as error:
		print 'Attribute'
	return str('')
	
def getTime(msg):
	#print 'getTime'
	global datestampGlobal
	try:
		datestampGlobal = msg.datestamp
	except AttributeError as error:
		pass
		#print 'datestamp not found'
	if 'datestampGlobal' in globals():
		res = '\r\t<time>' + datestampGlobal.strftime("%Y-%m-%d") + msg.timestamp.strftime("T%H:%M:%SZ") + '</time>'
		#print 'getTime:' + res
		return str(res)
	else:
		print 'NO TIME===='
		return str()

#fRead = open('test.csv', 'r')
fRead = open('180425-235321.csv', 'r') #long
#fRead = open('180427-041705.csv', 'r') #short
global fWrite
global writeName

def main():
	try: #best to use try/finally so that the file opens and closes correctly
		#getGPXHeader()
		#file = open('Failed.py', 'w')
		#file.write('whatever')
		#file.close()
		writeName  = 'test.gpx'
		file = open(writeName, 'w')
		file.write(str(getGPXHeader()))
		file.close()

		for line in fRead: #read each line in temp.txt
			#print line
			if line[:1] == '$':
				if '$GPGGA' in line and len(line) > 59:
					#if 'datestampGlobal' in globals():
					if len(writeName) > 0:
						#print 'GPGGA'
						file = open(writeName, 'a')
						file.write(getGPXPoint(line))
						file.close()
					continue
				elif '$GPRMC' in line and len(line) > 59:
					#print line
					#if 'writeName' in globals():
					if len(writeName) > 0:
						file = open(writeName, 'a')
						point = getGPXPoint(line)
						#print point
						file.write(point)
						file.close()
					#else:
						#writeName  = 'test.gpx'
						#file = open(writeName, 'w')
						#file.write(str(getGPXHeader()))
						#file.close()
					#print "=================="
					continue
				elif '$GPGLL' in line:
					#print line
					#msg = pynmea2.parse(line)
					#if 'writeName' in globals():
					if len(writeName) > 0:
						file = open(writeName, 'a')
						point = getGPXPoint(line)
						file.write(point)
						file.close()					
					#print msg.datestamp.strftime("%Y-%m-%d") + msg.timestamp.strftime("T%H:%M:%SZ")
					#print msg.timestamp
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
					#print msg.timestamp			
					continue
				else:
					#print line
					continue
	finally:
		fRead.close()
	file = open(writeName, 'a')
	file.write(getGPXEnder())
	file.close()
	
if __name__ == '__main__':
    main()	