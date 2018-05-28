#!/usr/bin/python
import serial
import inspect
import logging
import datetime
from datetime import datetime

#with open('/home/pi/dev/navi/Fusion.text', 'a') as file:
#        file.write('OK!\r\n')

#####Global Variables######################################
#be sure to declare the variable as 'global var' in the fxn
ser = 0

def function_logger(file_level, console_level = None):
    function_name = inspect.stack()[1][3]
    logger = logging.getLogger(function_name)
    logger.setLevel(logging.DEBUG) #By default, logs all messages

    if console_level != None:
        ch = logging.StreamHandler() #StreamHandler logs to console
        ch.setLevel(console_level)
        ch_format = logging.Formatter('%(asctime)s - %(message)s')
        ch.setFormatter(ch_format)
        logger.addHandler(ch)

    #fh = logging.FileHandler("{0}.log".format(function_name))
    fh = logging.FileHandler("/home/pi/dev/navi/one.log".format(function_name))
    fh.setLevel(file_level)
    fh_format = logging.Formatter('%(asctime)s - %(lineno)d - %(levelname)-8s - %(message)s')
    fh.setFormatter(fh_format)
    logger.addHandler(fh)
    return logger

#####FUNCTIONS#############################################
#initialize serial connection 
def init_serial_GPS():
        #COMNUM = 9 #set you COM port # here
        global serGps #must be declared in each fxn used
        serGps = serial.Serial()
        serGps.baudrate = 9600
        #ser.port = COMNUM - 1 #starts at 0, so subtract 1
        serGps.port = '/dev/ttyACM0' #uncomment for linux
        #you must specify a timeout (in seconds) so that the
        # serial port doesn't hang
        serGps.timeout = 1
	try:
        	serGps.open() #open the serial port
	        # print port open or closed
        	if serGps.isOpen():
	            print 'Open GPS: ' + serGps.portstr
	            f1_logger.info('Open GPS: ' + serGps.portstr)
	except Exception, e:
	    print 'error open serial port: ' + str(e)
            f1_logger.info('error open serial port: ' + str(e))
	    exit()

#initialize serial connection 
def init_serial_Arduino():
        global serArduino #must be declared in each fxn used
        serArduino = serial.Serial()
        serArduino.baudrate = 9600
        #ser.port = COMNUM - 1 #starts at 0, so subtract 1
        serArduino.port = '/dev/ttyUSB0' #uncomment for linux
        #you must specify a timeout (in seconds) so that the
        # serial port doesn't hang
        serArduino.timeout = 1
	try:
        	serArduino.open() #open the serial port
	        # print port open or closed
	        if serArduino.isOpen():
        	    print 'Open Arduino: ' + serArduino.portstr
                    f1_logger.info('Open Arduino: ' + serArduino.portstr)
	except Exception, e:
	    print "error open serial port: " + str(e)
            f1_logger.info('error open serial port: ' + str(e))
	    exit()

#####SETUP################################################
#this is a good spot to run your initializations 
global f1_logger
f1_logger = function_logger(logging.DEBUG, logging.ERROR)
init_serial_GPS()
init_serial_Arduino()
#####MAIN LOOP############################################

global fileName
fileName = datetime.now().strftime("%y%m%d-%H%M%S") + '.csv'

while 1:
    #prints what is sent in on the serial port
    #temp = raw_input('Type what you want to send, hit enter:\n\r')
    #ser.write(temp) #write to the serial port
    try:
        dataGPS = serGps.readline() #reads in bytes followed by a newline
        dataArduino = serArduino.readline() #reads in bytes followed by a newline  
    except Exception, e:
	    print "error read serial port: " + str(e)
            f1_logger.info('error open serial port: ' + str(e))
	    exit()
    with open("/home/pi/dev/navi/" + fileName, "a") as text_file:
	text_file.write('{} {}'.format(dataGPS, dataArduino))
	#'{} {}'.format(1, 2)
        #text_file.write("%s|%s" dataGPS, dataArduino)

    print 'write: ' + dataGPS + dataArduino
    #print 'You sent: ' + bytes
    #print to the console
    #break #jump out of loop 
#hit ctr-c to close python window
