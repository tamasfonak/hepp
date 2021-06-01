from http.client import HTTPConnection
import urllib
import multicast
import random

params = { 
	'token': 0,
	'distance': 0,
	'starting': 0, 
	'total': 0,
}
headers = { 
	'Content-type': 'application/x-www-form-urlencoded', 
	'Accept': 'text/plain' 
}

def compute_token( starting = 0, total = 0 ):
	print( "Hasn't been defined!" )

token = compute_token

def set_token():
	val = videos( params[ 'starting' ], params[ 'total' ] )
	params[ 'starting' ] = val[ 0 ]
	params[ 'total' ] = val[ 1 ]

def connect():
	while len( multicast.ips ) < 1:
		pass
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
