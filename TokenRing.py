import _thread
import token_listening
import token_sending

token = input( "Do I start with the token? y/n: " )
if token == "y":
	token_sending.params[ 'token' ] = 1
elif token == "n":
	token_sending.params[ 'token' ] == 0
	
def main_route():
	text = request.form[ 'token' ]
	if ( text == '1' ):
		token_sending.params[ 'token' ] = 1
		#token_sending.params[ 'distance' ] = request.form[ 'distance' ]
		#token_sending.params[ 'total' ] = int( request.form[ 'total' ] )
	_thread.start_new_thread( token_sending.send_token, () )
	return True

def start():
	_thread.start_new_thread( token_sending.multicast.receive, () )
	_thread.start_new_thread( token_sending.multicast.send, () )
	_thread.start_new_thread( token_listening.run, () )
	if ( token_sending.params[ 'token' ] == 1 ):
		token_sending.send_token()
