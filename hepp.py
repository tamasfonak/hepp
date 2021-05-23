import TokenRing
import math


def is_prime(num):
	"""Check if integer is prime

	Arguments:
	num -- integer to check
	"""
	for j in range(2, int(math.sqrt(num)+1)):
		if (num%j) == 0:
			return False
	if (num==0 or num==1):
		return False
	return True

def compute_primes( starting=0, _total=0 ):
	"""Check 100,000 integers for primes

   	Arguments:
    starting --  first prime to compute
    _total -- total number of primes up to starting
    """
	print ( "Starting: " + str( starting ) )
	print ( "Total: " + str( _total ) )
	total = _total
	ending = starting + 100000
	for i in range( starting, ending ):
		if is_prime( i ):
			total += 1
	print( "Ending: " + str( ending ) )
	print( "Total: " + str( total ) )
	# Returns a tuple containing ending value and total number up primes up to ending value
	return ( ending, total )



TokenRing.token_sending.primes = compute_primes
TokenRing.start()
