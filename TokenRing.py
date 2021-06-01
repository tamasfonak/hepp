from flask import Flask
from flask import request
import _thread
import token_sending

app = Flask(__name__)

token = input( "Do I start with the token? y/n: " )
if token == "y":
	token_sending.params[ 'token' ] = 1
elif token == "n":
	token_sending.params[ 'token' ] == 0

@app.before_first_request
def activate_job():
	if ( token_sending.params[ 'token' ] == 1 ):
		token_sending.send_token()
	else:
		pass
	
@app.route( '/', methods=['POST'] )
def my_form_post():
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
