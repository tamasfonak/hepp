import measure
import _thread 

_thread.start_new_thread( measure.start, () ) 

while True:
	print( measure.distance )
	measure.time.sleep( 0.1 )
