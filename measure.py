import RPi.GPIO as GPIO
import time

GPIO.setwarnings( False )
GPIO.setmode( GPIO.BCM )
GPIO_TRIGGER = 15
GPIO_ECHO = 18
GPIO_INTRUDER = 4
GPIO.setup( GPIO_TRIGGER, GPIO.OUT )
GPIO.setup( GPIO_ECHO, GPIO.IN )
GPIO.setup( GPIO_INTRUDER, GPIO.IN )

distance = 300
dfifo = [ 300, 300, 300, 300, 300, 300, 300, 300 ]
intruder = False
ififo = [ 0, 0, 0, 0, 0, 0, 0, 0 ]

def dist():
	GPIO.output( GPIO_TRIGGER, True )
	time.sleep( 0.00001 )
	GPIO.output( GPIO_TRIGGER, False )
	StartTime = time.time()
	StopTime = time.time()
	while GPIO.input( GPIO_ECHO ) == 0:
		StartTime = time.time()
	while GPIO.input( GPIO_ECHO ) == 1:
		StopTime = time.time()
	# time difference between start and arrival
	# multiply with the sonic speed ( 34300 cm/s )
	# and divide by 2, because there and back
	return int( ( ( StopTime - StartTime ) * 34300 ) / 2 )

def start():
	global distance
	while True:
		dfifo.append( dist() )
		dfifo.pop( 0 )
		distance = int( sum( dfifo ) / len( dfifo ) )
		ififo.append( int( GPIO.input( GPIO_INTRUDER ) ) )
		ififo.pop( 0 )
		intruder = sum( ififo )
		print( ififo )
		time.sleep( 0.2 )
