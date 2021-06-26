import socket
import binascii
import time
import threading
import _thread
import get_ip
import json

alive = {}
status = {}
now = 'waiting'

lock = threading.Lock()

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

def call_hepp():
	global now
	print( 'HEPP' );
	time.sleep( 5 )
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
			print( 'Received: ', sta.decode(), ' From: ', addr )
			print( 'Alive: ', alive )
			print( '---------------------')
			now = sta.decode()
			try:
				for ip in alive.keys():
					if ( time.time() - alive[ ip ] ) > 5:
						alive.pop( ip )
			except:
				pass
			lock.release()

		except socket.error:
      			print( 'socket.error: ', binascii.hexlify( data ) )

def send():
	host = get_ip.get_lan_ip()

	sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP )
	sock.setsockopt( socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32 )
	sock.setsockopt( socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton( host ) )

	while True:
		global now
		if now == 'waiting':
			now = 'passing'
		print( 'Status:', status )
		for ip in status.keys():
			if status[ ip ] == 'processing':
				now = 'waiting'
		if now == 'passing':
			now = 'processing'
			_thread.start_new_thread( call_hepp, () )

		sock.sendto( now.encode(), ( MCAST_GRP, MCAST_PORT ) )
		print( 'Sent: ', now )
		print( '+++++++++++++++++++++' )
		time.sleep( 3 )
