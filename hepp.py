import TokenRing
from omxplayer.player import OMXPlayer
from pathlib import Path
#import Measure
videos = {
	'floorLoop': Path( '/home/pi/hepp_videos/ures.mp4' ),
	'tableComesIn': Path( '/home/pi/hepp_videos/tabla_jon.mp4' ),
	'tableLoop': Path( '/home/pi/hepp_videos/ures_tabla.mp4' ),
	'tableGoesOut': Path( '/home/pi/hepp_videos/tabla_ki.mp4' )
}

loop = OMXPlayer( videos[ 'floorLoop' ], args=['--loop'], dbus_name='org.mpris.MediaPlayer2.loop' )
hepp = OMXPlayer( videos[ 'tableComesIn' ], dbus_name='org.mpris.MediaPlayer2.hepp' )
hepp.pause()

def compute_token( params ):
	print( params )
	return ( params )

TokenRing.token_sending.videos = compute_token
TokenRing.start()
app.run( port = 5000, host='0.0.0.0' )
