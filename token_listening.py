from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import cgi
import time

class Server(BaseHTTPRequestHandler):
    def _set_headers( self ):
        self.send_response( 200 )
        self.send_header( 'Content-type', 'application/json' )
        self.end_headers()
    def do_HEAD( self ):
        self._set_headers()
    def do_GET( self ):
        self._set_headers()
        self.wfile.write( json.dumps( { 'hello': 'world', 'received': 'ok' } ).encode() )
    def do_POST( self ):
        ctype, pdict = cgi.parse_header( self.headers.getheader( 'content-type' ) )
        if ctype != 'application/json':
            self.send_response( 400 )
            self.end_headers()
            return
        length = int( self.headers.getheader( 'content-length' ) )
        message = json.loads( self.rfile.read( length ) )
        message[ 'received' ] = 'ok'
        self._set_headers()
        self.wfile.write( json.dumps( message ).encode() )
        
def run( server_class=HTTPServer, handler_class=Server, port=5000 ):
    server_address = ( '', port )
    httpd = server_class( server_address, handler_class ) 
    print ( 'Starting httpd on port: ',  port )
    httpd.serve_forever()
