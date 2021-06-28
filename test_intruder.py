import RPi.GPIO as GPIO
import time

GPIO.setwarnings( False )
GPIO.setmode( GPIO.BCM )
GPIO_INTRUDER = 4
GPIO.setup( GPIO_INTRUDER, GPIO.IN )

while True:
	i = GPIO.input( GPIO_INTRUDER )
	if i == 1:
		print( 'Intruder' )
	else:
		print( '.' )
	time.sleep( 0.1 )
