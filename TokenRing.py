from flask import Flask
from flask import request
import _thread
import token_sending
import screen_color
import logging

log = logging.getLogger( 'werkzeug' )
log.setLevel( logging.ERROR )

app = Flask(__name__)

token = input( "Do I start with the token? y/n: " )
if token == "y":
	token_sending.params[ 'token' ] = 1
elif token == "n":
	token_sending.params[ 'token' ] == 0

@app.route( '/', methods=['POST'] )

def my_form_post():
	text = request.form[ 'token' ]
	if ( text == '1' ):
		token_sending.params[ 'token' ] = 1
		token_sending.params[ 'starting' ] = int( request.form[ 'starting' ] )
		token_sending.params[ 'total' ] = int( request.form[ 'total' ] )
		token_sending.screen_color.color( "green" )
	_thread.start_new_thread( token_sending.send_token, () )
	return 1


def start():
	_thread.start_new_thread( token_sending.multicast_receiver.receive, () )
	_thread.start_new_thread( token_sending.multicast_sender.send, () )
	if ( token_sending.params[ 'token' ] == 1 ):
		token_sending.screen_color.color( "green" )
		token_sending.send_token()
	else:
		token_sending.screen_color.color( "red" )
		pass

	app.run( port = 5000, host='0.0.0.0' )
