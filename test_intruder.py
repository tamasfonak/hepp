import measure
import _thread 

_thread.start_new_thread( measure.start, () ) 

while True:
	if measure.intruder > 5:
		print( 'intruder' )
	measure.time.sleep( 1 )
