import measure
import _thread 

_thread.start_new_thread( measure.start, () ) 

while True:
	measure.time.sleep( 0.1 )
