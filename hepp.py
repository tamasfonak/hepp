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

loop = OMXPlayer( videos[ 'floorLoop' ], args = [ '--loop' ], dbus_name = 'org.mpris.MediaPlayer2.loop' )
hepp = OMXPlayer( videos[ 'tableComesIn' ], dbus_name='org.mpris.MediaPlayer2.hepp', pause = False )
hepp = False
isHepp = False

def loopLoad( loopPath ):
	loop.load( loopPath )
	loop.pause()
	return True

def compute_video():
	hepp.play()

        loop.load( videos[ 'tableLoop' ] )

        loop.pause()
        isHepp = True;
        while hepp.duration() > hepp.position() + 1:
                pass
        hepp.pause()
        isHepp = False;
        loop.play()

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
