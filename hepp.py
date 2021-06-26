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
	'30': '/home/pi/hepp_videos/HEPP_POCOK_30.mp4',
	'29': '/home/pi/hepp_videos/HEPP_POCOK_29.mp4',
	'28': '/home/pi/hepp_videos/HEPP_POCOK_28.mp4',
	'27': '/home/pi/hepp_videos/HEPP_POCOK_27.mp4',
	'26': '/home/pi/hepp_videos/HEPP_POCOK_26.mp4',
	'25': '/home/pi/hepp_videos/HEPP_POCOK_25.mp4',
	'24': '/home/pi/hepp_videos/HEPP_POCOK_24.mp4',
	'23': '/home/pi/hepp_videos/HEPP_POCOK_23.mp4',
	'22': '/home/pi/hepp_videos/HEPP_POCOK_22.mp4',
	'21': '/home/pi/hepp_videos/HEPP_POCOK_21.mp4',
	'20': '/home/pi/hepp_videos/HEPP_POCOK_20.mp4',
	'19': '/home/pi/hepp_videos/HEPP_POCOK_19.mp4',
	'18': '/home/pi/hepp_videos/HEPP_POCOK_18.mp4',
	'17': '/home/pi/hepp_videos/HEPP_POCOK_17.mp4',
	'16': '/home/pi/hepp_videos/HEPP_POCOK_16.mp4',
	'15': '/home/pi/hepp_videos/HEPP_POCOK_15.mp4',
	'14': '/home/pi/hepp_videos/HEPP_POCOK_14.mp4',
	'13': '/home/pi/hepp_videos/HEPP_POCOK_13.mp4',
	'12': '/home/pi/hepp_videos/HEPP_POCOK_12.mp4',
	'11': '/home/pi/hepp_videos/HEPP_POCOK_11.mp4',
	'10': '/home/pi/hepp_videos/HEPP_POCOK_10.mp4',
	'9': '/home/pi/hepp_videos/HEPP_POCOK_9.mp4',
	'8': '/home/pi/hepp_videos/HEPP_POCOK_8.mp4',
	'7': '/home/pi/hepp_videos/HEPP_POCOK_7.mp4',
	'6': '/home/pi/hepp_videos/HEPP_POCOK_6.mp4',
	'5': '/home/pi/hepp_videos/HEPP_POCOK_5.mp4',
	'4': '/home/pi/hepp_videos/HEPP_POCOK_4.mp4',
	'3': '/home/pi/hepp_videos/HEPP_POCOK_3.mp4',
	'2': '/home/pi/hepp_videos/HEPP_POCOK_2.mp4',
	'1': '/home/pi/hepp_videos/HEPP_POCOK_1.mp4'
}

#loop = OMXPlayer( Path( videos[ 'floorLoop' ] ), args = [ '--no-osd', '--loop', '--layer', '0', '--win', '0,0,1920,1080' ], dbus_name = 'org.mpris.MediaPlayer2.loop' )

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
#_thread.start_new_thread( tokening.multicast.send, () )
#_thread.start_new_thread( tokening.listen, () )

try:
	while True:
		pass #play_hepp( videos[ str( random.randint( 1, 30 ) ) ] )

except KeyboardInterrupt:
        print( 'interrupted!' )
        _thread.exit()
        print( 'stopped!' )
