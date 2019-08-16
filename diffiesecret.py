sharedprime = 97
sharedbase = 51

def calculate_shared(secret):
	'''
	Calculates the public key.
	Parameters:
 	secret = user's private key
	'''
	return str((sharedbase ** secret) % sharedprime)

def calculate_secret(received, secret):
	'''
	Calculates the shared secret key.
	Parameters:
	received = public key
	secret = user's private key
	'''
	return str((int(received) ** secret) % sharedprime)
