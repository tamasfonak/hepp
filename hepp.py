
from omxplayer.player import OMXPlayer
from pathlib import Path
import _thread
import tokening
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

def main_route():
	text = request.form[ 'token' ]
	if ( text == '1' ):
		tokening.params[ 'token' ] = 1
		#token_sending.params[ 'distance' ] = request.form[ 'distance' ]
		#token_sending.params[ 'total' ] = int( request.form[ 'total' ] )
	_thread.start_new_thread( tokening.send_token, () )
	return True

tokening.token = compute_token
_thread.start_new_thread( tokening.multicast.receive, () )
_thread.start_new_thread( tokening.multicast.send, () )
_thread.start_new_thread( tokening.listen, () )
if ( tokening.params[ 'token' ] == 1 ):
	tokening.send_token()
