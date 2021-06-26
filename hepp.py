import logging 
import random
from omxplayer.player import OMXPlayer 
from pathlib import Path 
import _thread 
import distance
import socket
import time
import threading
import get_ip

logging.basicConfig( level = logging.INFO )

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

lock = threading.Lock()

alive = {}
status = {}
now = 'passing'
hepp = 0

def compute_token():
	global now, hepp
	hepp += 1
	print( "HEPP", hepp )
	time.sleep( 3 )
	#play_hepp( videos[ str( random.randint( 1, 30 ) ) ] )
	now = 'passing'
	return True

def receive():
	host = get_ip.get_lan_ip()
	sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP )
	try:
		sock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
	except AttributeError as error:
		print ( 'AttributeError: ', error )
	sock.setsockopt( socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32 )
	sock.setsockopt( socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1 )
	sock.bind( ( MCAST_GRP, MCAST_PORT ) )
	sock.setsockopt( socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton( host ) )
	sock.setsockopt( socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton( MCAST_GRP ) + socket.inet_aton( host ) )
	while True:
		global now
		try:
			sta, ( addr, port ) = sock.recvfrom( 1024 )
			lock.acquire()
			if addr != host:
				alive[ addr ] = time.time()
				status[ addr ] = sta.decode()
			try:
				for ip in alive.keys():
					if ( time.time() - alive[ ip ] ) > 3:
						alive.pop( ip )
						status.pop( ip )
			except:
				pass
			lock.release()
		except socket.error:
      			print( 'socket.error!!!')

def send():
	host = get_ip.get_lan_ip()
	sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP )
	sock.setsockopt( socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32 )
	sock.setsockopt( socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton( host ) )
	while True:
		global now
		for ip in status.keys():
			if status[ ip ] == 'processing':
				now = 'waiting'
			elif status[ ip ] == 'passing': 
				now = 'passing'
		if now == 'passing':
			now = 'processing'
			_thread.start_new_thread( compute_token, () )
		try:
			sock.sendto( now.encode(), ( MCAST_GRP, MCAST_PORT ) )
		except: 
			print( 'Network error!!!!' )
		time.sleep( 0.1 )
		
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
	return True

_thread.start_new_thread(  receive, () )
_thread.start_new_thread(  send, () )

try:
	while True:
		time.sleep( 1 )

except KeyboardInterrupt:
        print( 'interrupted!' )
        _thread.exit()
        print( 'stopped!' )
