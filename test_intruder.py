import measure

while True:
	if measure.intruder():
		print( 'Intruder: ', measure.intruder() )
	else:
		print( measure.distance() )
	measure.time.sleep( 0.1 )
