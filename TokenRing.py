from flask import Flask
from flask import request

import _thread
import token_sending

token = input( "Do I start with the token? y/n: " )
if token == "y":
	token_sending.params[ 'token' ] = 1
elif token == "n":
	token_sending.params[ 'token' ] == 0

app = Flask(__name__)

@app.before_first_request
def activate_job():
	app.logger.info( "activate_job" )
	if ( token_sending.params[ 'token' ] == 1 ):
		token_sending.send_token()
	
@app.route( '/', methods=['POST'] )
def main_route():
	app.logger.info( "main route" )
	text = request.form[ 'token' ]
	if ( text == '1' ):
		token_sending.params[ 'token' ] = 1
		#token_sending.params[ 'distance' ] = request.form[ 'distance' ] )
		#token_sending.params[ 'total' ] = int( request.form[ 'total' ] )
	_thread.start_new_thread( token_sending.send_token, () )
	return True

def start():
	_thread.start_new_thread( token_sending.multicast.receive, () )
	_thread.start_new_thread( token_sending.multicast.send, () )
	app.run( port = 5000, host='0.0.0.0' )
