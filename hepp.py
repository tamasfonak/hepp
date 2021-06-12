import logging
from omxplayer.player import OMXPlayer
from pathlib import Path
import _thread
import tokening
import distance

logging.basicConfig( level = logging.INFO )

videos = {
        'floorLoop': '/home/pi/hepp_videos/ures.mp4',
        'tableComesIn': '/home/pi/hepp_videos/tabla_jon.mp4',
        'tableLoop': '/home/pi/hepp_videos/ures_tabla.mp4',
        'tableGoesOut': '/home/pi/hepp_videos/tabla_ki.mp4'
}

loop = OMXPlayer( Path( videos[ 'floorLoop' ] ), args = [ '--no-osd', '--loop', '--layer', '0' ], dbus_name = 'org.mpris.MediaPlayer2.loop' )

isHepp = False

def play_hepp( heppFile, loopFile = False ):
        isHepp = True
        hepp = OMXPlayer( Path( heppFile ), args = [ '--no-osd', '--layer', '1' ], dbus_name='org.mpris.MediaPlayer2.hepp' )
        while hepp.position() < 1:
                pass
        if loopFile:
                loop.load( Path( loopFile ) )
        while hepp.duration() > hepp.position() + 1:
                pass
        tokening.params[ 'token' ] = 1
        isHepp = False
        return True

def compute_token( params ):
        if params[ 'token' ] == 1 and isHepp == False:
                pass #play_hepp()
        return ( params )

tokening.set_token = compute_token

_thread.start_new_thread( tokening.multicast.receive, () )
_thread.start_new_thread( tokening.multicast.send, () )
_thread.start_new_thread( tokening.listen, () )

#tokening.time.sleep( 3 )

#play_hepp( videos[ 'tableComesIn' ], videos[ 'tableLoop' ] )

#tokening.time.sleep( 3 )

#play_hepp( videos[ 'tableGoesOut' ], videos[ 'floorLoop' ] )

while True:
        #print( distance.measure() )
        tokening.time.sleep( 1 )
