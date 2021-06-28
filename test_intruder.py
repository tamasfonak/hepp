import measure

while True:
	if measure.intruder:
		print( 'Intruder' )
	else:
		print( measure.distance() )
	measure.time.sleep( 0.1 )
