from http.client import HTTPConnection
import urllib
import multicast
import random

params = { token: 1 }
headers = { 
	'Content-type': 'application/x-www-form-urlencoded', 
	'Accept': 'text/plain' 
}

def compute_token( params ):
	print( "Hasn't been defined!" )

token = compute_token

def set_token():
	val = token( params )
	params[ 'starting' ] = val[ 0 ]
	params[ 'total' ] = val[ 1 ]

def connect():
	while len( multicast.ips ) < 1:
		pass # Ez a ciklus fut mi'g nincs ma'sik ge'pa a ha'lo'zaton. (Ha a saja't IP-t kiza'rom)
	try:
		multicast.lock.acquire()
		connection = HTTPConnection( random.choice( list( multicast.ips.keys() ) ), 5000, timeout=10 )
		multicast.lock.release()
		connection.request( "POST", "/", urllib.parse.urlencode( params ), headers )
		response = connection.getresponse()
		return True
	except multicast.socket.error:
		return connect()

def send_token():
	set_token()
	if connect() == False:
		print( "Something went wrong" )
	else:
		params[ 'token' ] = 0
	return True
