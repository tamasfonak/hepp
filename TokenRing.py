from flask import Flask
from flask import request
from flask_script import Manager, Server

import _thread
import token_sending

app = Flask(__name__)
manager = Manager( app )

token = input( "Do I start with the token? y/n: " )
if token == "y":
	token_sending.params[ 'token' ] = 1
elif token == "n":
	token_sending.params[ 'token' ] == 0

def activate_job():
	if ( token_sending.params[ 'token' ] == 1 ):
		token_sending.send_token()
	else:
		pass
class CustomServer(Server):
    def __call__(self, app, *args, **kwargs):
        activate_job()
        #Hint: Here you could manipulate app
        return Server.__call__(self, app, *args, **kwargs)

manager.add_command( 'runserver', CustomServer() )
	
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
	manager.run( port = 5000, host='0.0.0.0' )
