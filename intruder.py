import RPi.GPIO as GPIO
import time
GPIO.setwarnings( False )
GPIO.setmode( GPIO.BCM )
GPIO.setup( 4, GPIO.IN )

while True:
	
	i = GPIO.input( 17 )
	if i==1:
		print( 'Intruder' )
	time.sleep( 0.1 )
	print( '' )
