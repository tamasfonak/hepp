import measure
import _thread 

_thread.start_new_thread( measure.start, () ) 

while True:
	print( measure.intruder() )
	measure.time.sleep( 0.1 )
