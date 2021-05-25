import TokenRing
from omxplayer.player import OMXPlayer
from pathlib import Path
#import Measure
videos = {
	'floorLoop': Path('./floorLoop.mp4' ),
	'tableComesIn': Path('./tableComesIn.mp4' ),
	'tableLoop': Path('./tableLoop.mp4' ),
	'tableGoesOut': Path('./tableGoesOut.mp4' )
}

loop = OMXPlayer( videos.floorLoop, dbus_name='org.mpris.MediaPlayer2.loop' )
hepp = OMXPlayer( videos.tableComesIn, dbus_name='org.mpris.MediaPlayer2.hepp' )
hepp.pause()

def compute_videos( starting = 0, total = 0 ):
	# measure.distance()
	return ( starting, total )

TokenRing.token_sending.videos = compute_videos
TokenRing.start()
