import os
import socket

if os.name != "nt":
	import fcntl
	import struct
	def get_interface_ip( ifname ):
        	s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        	return socket.inet_ntoa( fcntl.ioctl(
                	s.fileno(),
                	0x8915,  # SIOCGIFADDR
                	struct.pack( '256s', bytes( ifname[:15], 'utf-8' ) )
            	) [20:24] )

def get_lan_ip():
    	ip = socket.gethostbyname( socket.gethostname() )
    	if ip.startswith( "127." ) and os.name != "nt":
        	interfaces = [ "wlan0", "wlan1", "wifi0", "ath0", "ath1", "ppp0", "eth0", "eth1", "eth2" ]
        	for ifname in interfaces:
            		try:
                		ip = get_interface_ip( ifname )
                		break;
            		except IOError:
                		pass
    	return ip
