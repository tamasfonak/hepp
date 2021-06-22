import logging 
import random
from omxplayer.player import OMXPlayer 
from pathlib import Path 
import _thread 
import tokening 
import distance

logging.basicConfig( level = logging.INFO )


videos = {
        'floorLoop': '/home/pi/hepp_videos/URES_MANEZS_HOSSZU_CBR_10M.mp4',
        'tableComesIn': '/home/pi/hepp_videos/01_tabla_BE.mp4',
        'tableLoop': '/home/pi/hepp_videos/01_tabla_TABLA.mp4',
        'tableGoesOut': '/home/pi/hepp_videos/01_tabla_OUT.mp4',
	'19': '/home/pi/hepp_videos/HEPP_POCOK_19.mp4',
	'18': '/home/pi/hepp_videos/HEPP_POCOK_18.mp4',
	'17': '/home/pi/hepp_videos/HEPP_POCOK_17.mp4',
	'16': '/home/pi/hepp_videos/HEPP_POCOK_16.mp4',
	'15': '/home/pi/hepp_videos/HEPP_POCOK_15.mp4',
	'14': '/home/pi/hepp_videos/HEPP_POCOK_14.mp4'
}

loop = OMXPlayer( Path( videos[ 'floorLoop' ] ), args = [ '--no-osd', '--loop', '--layer', '0', '--win', '0,0,1920,1080' ], dbus_name = 'org.mpris.MediaPlayer2.loop' )

def play_hepp( heppFile, loopFile = False ):
	hepp = OMXPlayer( Path( heppFile ), args = [ '--no-osd', '--layer', '1', '--win', '0,0,1920,1080', '--alpha', '0' ], dbus_name='org.mpris.MediaPlayer2.hepp' )
	while hepp.position() < 1:
		alpha = int( hepp.position() * 255 )
		if alpha < 255 and alpha > 0:
			hepp.set_alpha( alpha )
	while hepp.position() < 1.5:
		hepp.set_alpha( 255 )
	if loopFile:
		loop.load( Path( loopFile ) )
	while hepp.duration() > hepp.position() + 0.3:
		alpha = int( ( hepp.duration() - hepp.position() ) * 255 )
		if alpha < 255 and alpha > 0:
			hepp.set_alpha( alpha )
	hepp.set_alpha( 0 )
	hepp.quit()
	tokening.params[ 'token' ] = 1
	return True

def compute_token( params ):
        print( "hepp" )
        tokening.time.sleep( 1 )
        params[ 'token' ] = 1
        return ( params )

tokening.set_token = compute_token

_thread.start_new_thread( tokening.multicast.receive, () )
_thread.start_new_thread( tokening.multicast.send, () )
_thread.start_new_thread( tokening.listen, () )

try:
	while True:
		tokening.time.sleep( 3 )
		play_hepp( videos[ str( random.randint( 14, 19 ) ) ] )

except KeyboardInterrupt:
        print( 'interrupted!' )
        _thread.exit()
        print( 'stopped!' )
