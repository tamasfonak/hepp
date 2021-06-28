#!/usr/bin/python3

import logging 
import random
from omxplayer.player import OMXPlayer 
from pathlib import Path 
import _thread 
import measure
import socket
import time
import threading
import get_ip

logging.basicConfig( level = logging.INFO )

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

lock = threading.Lock()

alive = {}
neighborhood = {}
status = 'waiting'
hepp = 0

videoPath = '/home/pi/hepp_videos/CBR10/'
porond = videoPath + 'URES_MANEZS.mp4' 
tables = {
	1: {
		'tableLoop': videoPath + '01_tabla.mp4',
		'tableCI': videoPath + '01_tabla_BE.mp4',
		'tableGO': videoPath + '01_tabla_KI.mp4'
	},
	2: {
		'tableLoop': videoPath + '02_tabla.mp4',
		'tableCI': videoPath + '02_tabla_BE.mp4',
		'tableGO': videoPath + '02_tabla_KI.mp4'
	},
	3:{
		'tableLoop': videoPath + '03_tabla.mp4',
		'tableCI': videoPath + '03_tabla_BE.mp4',
		'tableGO': videoPath + '03_tabla_KI.mp4'
	},
	4:{
		'tableLoop': videoPath + '04_tabla.mp4',
		'tableCI': videoPath + '04_tabla_BE.mp4',
		'tableGO': videoPath + '04_tabla_KI.mp4'
	}
}
hepps = {
	1: videoPath + 'HEPPek/HEPP_POCOK_01.mp4',
	2: videoPath + 'HEPPek/HEPP_POCOK_02.mp4',
	3: videoPath + 'HEPPek/HEPP_POCOK_03.mp4',
	4: videoPath + 'HEPPek/HEPP_POCOK_04.mp4',
	5: videoPath + 'HEPPek/HEPP_POCOK_05.mp4',
	6: videoPath + 'HEPPek/HEPP_POCOK_06.mp4',
	7: videoPath + 'HEPPek/HEPP_POCOK_07.mp4',
	8: videoPath + 'HEPPek/HEPP_POCOK_08.mp4',
	9: videoPath + 'HEPPek/HEPP_POCOK_09.mp4',
	10: videoPath + 'HEPPek/HEPP_POCOK_10.mp4',
	11: videoPath + 'HEPPek/HEPP_POCOK_11.mp4',
	12: videoPath + 'HEPPek/HEPP_POCOK_12.mp4',
	13: videoPath + 'HEPPek/HEPP_POCOK_13.mp4',
	14: videoPath + 'HEPPek/HEPP_POCOK_14.mp4',
	15: videoPath + 'HEPPek/HEPP_POCOK_15.mp4',
	16: videoPath + 'HEPPek/HEPP_POCOK_16.mp4',
	17: videoPath + 'HEPPek/HEPP_POCOK_17.mp4',
	18: videoPath + 'HEPPek/HEPP_POCOK_18.mp4',
	19: videoPath + 'HEPPek/HEPP_POCOK_19.mp4',
	20: videoPath + 'HEPPek/HEPP_POCOK_20.mp4',
	21: videoPath + 'HEPPek/HEPP_POCOK_21.mp4',
	22: videoPath + 'HEPPek/HEPP_POCOK_22.mp4',
	23: videoPath + 'HEPPek/HEPP_POCOK_23.mp4',
	24: videoPath + 'HEPPek/HEPP_POCOK_24.mp4',
	25: videoPath + 'HEPPek/HEPP_POCOK_25.mp4',
	26: videoPath + 'HEPPek/HEPP_POCOK_26.mp4',
	27: videoPath + 'HEPPek/HEPP_POCOK_27.mp4',
	28: videoPath + 'HEPPek/HEPP_POCOK_28.mp4',
	29: videoPath + 'HEPPek/HEPP_POCOK_29.mp4',
	30: videoPath + 'HEPPek/HEPP_POCOK_30.mp4',
	31: videoPath + 'HEPPek/HEPP_POCOK_31.mp4',
	32: videoPath + 'HEPPek/HEPP_POCOK_32.mp4',
	33: videoPath + 'HEPPek/HEPP_POCOK_33.mp4',
	34: videoPath + 'HEPPek/HEPP_POCOK_34.mp4',
	35: videoPath + 'HEPPek/HEPP_POCOK_35.mp4',
	36: videoPath + 'HEPPek/HEPP_POCOK_36.mp4',
	37: videoPath + 'HEPPek/HEPP_POCOK_37.mp4',
	38: videoPath + 'HEPPek/HEPP_POCOK_38.mp4',
	39: videoPath + 'HEPPek/HEPP_POCOK_39.mp4',
	40: videoPath + 'HEPPek/HEPP_POCOK_40.mp4',
	41: videoPath + 'HEPPek/HEPP_POCOK_41.mp4',
	42: videoPath + 'HEPPek/HEPP_POCOK_42.mp4',
	43: videoPath + 'HEPPek/HEPP_POCOK_43.mp4',
	44: videoPath + 'HEPPek/HEPP_POCOK_44.mp4',
	45: videoPath + 'HEPPek/HEPP_POCOK_45.mp4',
	46: videoPath + 'HEPPek/HEPP_POCOK_46.mp4',
	47: videoPath + 'HEPPek/HEPP_POCOK_47.mp4',
	48: videoPath + 'HEPPek/HEPP_POCOK_48.mp4',
	49: videoPath + 'HEPPek/HEPP_POCOK_49.mp4'
}

loop = OMXPlayer( Path( porond ), args = [ '--no-osd', '--loop', '--layer', '0', '--win', '0,0,1920,1080' ], dbus_name = 'org.mpris.MediaPlayer2.loop' )

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
				print( '!!! neighborhood processing error !!!' )
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
		if now == 'waiting' and all( s == 'waiting' for s in status.values() ):
			now = 'processing'
			try:
				_thread.start_new_thread( compute_token, () )
			except: 
				print( '!!! compute_token thread starting error !!!' )
				now = 'passing'
		try:
			sock.sendto( now.encode(), ( MCAST_GRP, MCAST_PORT ) )
		except: 
			print( '!!! status send error !!!' )
		time.sleep( 1 )

def compute_token():
	global now, hepp
	hepp += 1
	if 'processing' in status.values():
		now = 'waiting'
		return True
	print( "HEPP", hepp, 'Status: ', status )
	try:
		play_hepp( hepps[ random.randint( 1, 49 ) ] )
	except:
		print( '!!! play_hepp except !!!' )
	now = 'waiting'
	return True	

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

_thread.start_new_thread(  receive, () ) # elkezdunk hallgatozni
time.sleep( 1 ) # varunk egy kicsit mielott beleszolunk
_thread.start_new_thread(  send, () )
_thread.start_new_thread(  measure.intruder, () )

try:
	while True:
		print( 'distance: ', measure.distance() )
		time.sleep( 1 )

except KeyboardInterrupt:
        print( 'interrupted!' )
        _thread.exit()
        print( 'stopped!' )
