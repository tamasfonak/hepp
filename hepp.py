import logging
from omxplayer.player import OMXPlayer
from pathlib import Path
import _thread
import tokening
#import Measure

logging.basicConfig( level = logging.DEBUG )

videos = {
	'floorLoop': Path( '/home/pi/hepp_videos/ures.mp4' ),
	'tableComesIn': Path( '/home/pi/hepp_videos/tabla_jon.mp4' ),
	'tableLoop': Path( '/home/pi/hepp_videos/ures_tabla.mp4' ),
	'tableGoesOut': Path( '/home/pi/hepp_videos/tabla_ki.mp4' )
}

loop = OMXPlayer( videos[ 'floorLoop' ], args = [ '--no-osd', '--loop', '--layer', '0' ], dbus_name = 'org.mpris.MediaPlayer2.loop', pause = True )
hepp = OMXPlayer( videos[ 'tableComesIn' ], args = [ '--no-osd', '--layer', '1' ], dbus_name='org.mpris.MediaPlayer2.hepp', pause = True )

isHepp = False

def compute_video():
        loop.play()
        tokening.time.sleep( 1 )
        hepp.play()
        loop.load( videos[ 'tableLoop' ], pause = True )
        isHepp = True;
        while hepp.duration() > hepp.position() + 0.5:
                pass #print( hepp.position() )
        loop.play()
        hepp.hide_video() # nem mukodik...
        hepp.pause()
        isHepp = False;
        tokening.params[ 'token' ] = 1
        return True
	
def compute_token( params ):
	if params[ 'token' ] == 1 and isHepp == False:
		_thread.start_new_thread( compute_video, () )
	return ( params )

tokening.set_token = compute_token
_thread.start_new_thread( tokening.multicast.receive, () )
_thread.start_new_thread( tokening.multicast.send, () )
_thread.start_new_thread( tokening.listen, () )

compute_video()

while True:
        pass
