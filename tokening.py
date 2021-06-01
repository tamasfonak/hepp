from http.server import BaseHTTPRequestHandler, HTTPServer
from http.client import HTTPConnection
import json
import cgi
import time
import _thread
import multicast
import random

params = { 'token': 1 }

class CallbackHTTPServer( HTTPServer ):
	def server_activate( self ):
		self.RequestHandlerClass.pre_start()
		HTTPServer.server_activate( self )
		self.RequestHandlerClass.post_start()

	def server_close( self ):
		self.RequestHandlerClass.pre_stop()
		HTTPServer.server_close( self )
		self.RequestHandlerClass.post_stop()

class HttpHandler( BaseHTTPRequestHandler ):
	@classmethod
	def pre_start(cls):
		print ('Before calling socket.listen()')

	@classmethod
	def post_start(cls):
		if ( params[ 'token' ] == 1 ):
			_thread.start_new_thread( send_token, () )
	@classmethod
	def pre_stop(cls):
		print ('Before calling socket.close()')
	@classmethod
	def post_stop(cls):
		print ('After calling socket.close()')
        
	def _set_headers( self ):
		self.send_response( 200 )
		self.send_header( 'Content-type', 'application/json' )
		self.end_headers()
	def do_HEAD( self ):
		self._set_headers()
	def do_GET( self ):
		self._set_headers()
		self.wfile.write( json.dumps( { 'HEPP': '0.1' } ).encode() )
	def do_POST( self ):
		ctype, pdict = cgi.parse_header( self.headers.get( 'content-type' ) )
		if ctype != 'application/json':
			self.send_response( 400 )
			self.end_headers()
			return
		length = int( self.headers.get( 'content-length' ) )
		message = json.loads( self.rfile.read( length ) )
		message[ 'token' ] = 1
		self._set_headers()
		self.wfile.write( json.dumps( message ).encode() )
		time.sleep( 3 )
		_thread.start_new_thread( send_token, () )
        
def listen():
	httpd = CallbackHTTPServer( ( '', 5000 ), HttpHandler ) 
	print ( 'Starting httpd on port: 5000')
	httpd.serve_forever()


headers = { 
	'Content-type': 'application/json', 
	'Accept': 'text/plain' 
}

def compute_token( params ):
	print( "Hasn't been defined!" )

token = compute_token

def set_token():
	val = token( params )
	#params[ 'token' ] = val[ 0 ]

def connect():
	while len( multicast.ips ) < 1:
		pass # Ez a ciklus fut mi'g nincs ma'sik ge'pa a ha'lo'zaton. (Ha a saja't IP-t kiza'rom)
	try:
		multicast.lock.acquire()
		connection = HTTPConnection( random.choice( list( multicast.ips.keys() ) ), 5000, timeout=10 )
		multicast.lock.release()
		connection.request( "POST", "/", json.dumps( params ), headers )
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
