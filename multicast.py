import socket
import binascii
import time
import threading
import _thread
import get_ip

ips = {}
lock = threading.Lock()

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

def alive():
	while True:
		for ip in ips.keys():
			lock.acquire()
			if ( time.time() - ips[ ip ] ) > 5:
				ips.pop( ip )
			lock.release()
		time.sleep( 5 )

def receive():
	_thread.start_new_thread( alive, () )
	
	host = get_ip.get_lan_ip()

	sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP )

	try:
		sock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
	except AttributeError as error:
		print ( error )

	sock.setsockopt( socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32 ) 
	sock.setsockopt( socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1 )
	sock.bind( ( MCAST_GRP, MCAST_PORT ) )
	sock.setsockopt( socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton( host ) )
	sock.setsockopt( socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton( MCAST_GRP ) + socket.inet_aton( host ) )
	
	while True:
		try:
			data.decode(), addr = sock.recvfrom( 1024 )
			#if data.decode() != host: # Saja't IP-k kiza'rom?
			lock.acquire()
			ips[ data ] = time.time()
			print( data )
			lock.release()
		except socket.error:
      			print( binascii.hexlify( data ) )

def send():
	host = get_ip.get_lan_ip()

	sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP )
	sock.setsockopt( socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32 )

	while True:
		sock.sendto( host.encode(), ( MCAST_GRP, MCAST_PORT ) )
		time.sleep( 3 )
