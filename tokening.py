from http.server import BaseHTTPRequestHandler, HTTPServer
from http.client import HTTPConnection
import json
import cgi
import time
import _thread
import multicast
import random

params = { 'token': 1 }

def compute_token( params ):
	print( "Hasn't been defined!" )

set_token = compute_token

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
	def pre_start( cls ):
		print ('Before calling socket.listen()')
	@classmethod
	def post_start( cls ):
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
		self.send_header( 'Accept', 'text/plain' )
		self.end_headers()
	def do_HEAD( self ):
		self._set_headers()
	def do_GET( self ):
		self._set_headers()
		self.wfile.write( json.dumps( params ).encode() )
	def do_POST( self ):
		ctype, pdict = cgi.parse_header( self.headers.get( 'content-type' ) )
		if ctype != 'application/json':
			self.send_response( 400 )
			self.end_headers()
			return
		length = int( self.headers.get( 'content-length' ) )
		params = json.loads( self.rfile.read( length ) )
		
		self._set_headers()
		self.wfile.write( json.dumps( params ).encode() )
        
def listen():
	#host = multicast.get_ip.get_lan_ip()
	multicast.lock.acquire()
	httpd = CallbackHTTPServer( ( '', 5000 ), HttpHandler ) 
	print ( 'Starting httpd on port: 5000')
	multicast.lock.release()
	httpd.serve_forever()

headers = { 
	'Content-type': 'application/json', 
	'Accept': 'text/plain' 
}

def connect():
	while len( multicast.ips ) < 1:
		time.sleep( 1 ) # Ez a ciklus fut mi'g nincs ma'sik ge'pa a ha'lo'zaton. (Ha a saja't IP-t kiza'rom)
	try:
		multicast.lock.acquire()
		connection = HTTPConnection( random.choice( list( multicast.ips.keys() ) ), 5000, timeout=10 )
		multicast.lock.release()
		connection.request( "POST", "/", json.dumps( params ), headers )
		
		response = connection.getresponse()
		
		data = json.loads( response.read().decode() )
		
		connection.close()
		
		if data[ 'token' ] == 0:
			time.sleep( 1 )
		else: 
			set_token( params )
			
		return True
	except multicast.socket.error:
		return connect()

def send_token():
	while connect() == True:
		pass
	return True
