import random
import socket
from diffiesecret import *
from AES_func import AES_func
import time
import string

DIR_PORT = "6677"
CLIENT_PORT = "6600"
NODE_PORTS = ["6665", "6664", "6663"]
KEYS = [] #Encryption keys for the nodes
HOST = "localhost"
OWNSECRET = 34 #For Diffie-Hellman key exchange
CLIENT_KEY = "" #Encryption key for directory-client communication
NODE_KEYS = {} #Encryption keys for directory-node communication
AES = AES_func()

def create_socket():
	'''Creates sockets'''
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	return s

def client_keyexchange():
	'''
	Performs Diffie-Hellman key exchange with the client 
	and creates AES encryption key based on the shared private key
	'''
	global CLIENT_KEY
	s = create_socket()
	s.bind((HOST, int(DIR_PORT)))
	s.listen(10)
	conn, addr = s.accept()
	msg = str(conn.recv(1024))
	conn.send(calculate_shared(OWNSECRET).encode('utf-8'))
	sharedsecret = calculate_secret(int(msg), OWNSECRET)
	CLIENT_KEY = AES.DF_keygen(sharedsecret)

def node_keyexchange():
	'''
	Performs Diffie-Hellman key exchange with the nodes and also tells the nodes
	their respective ports. Creates AES encryption keys based on the shared private keys.
	'''
	s = create_socket()
	s.bind((HOST, int(DIR_PORT)))
	s.listen(10)
	cons = 0
        while cons != 3:
                conn, addr = s.accept()
		cons += 1
		msg = str(conn.recv(1024))
		sharedsecret = calculate_secret(int(msg), OWNSECRET)
		port = NODE_PORTS[cons-1]
		NODE_KEYS[port] = AES.DF_keygen(sharedsecret)
		encrypted = AES.encrypt(port, NODE_KEYS[port])
		answer = calculate_shared(OWNSECRET) + "###" + str(encrypted)
		conn.send(answer.encode('utf-8'))

def create_keys():
	'''Creates the 16bit AES encryption keys for the nodes'''
	chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
        for i in range(3):
                key = ''.join(random.choice(chars) for i in range(16))
                KEYS.append(key)


def key_distribution():
	'''
	Chooses the order of the nodes.
	Sends an encrypted message to the nodes that contains:
	Node's AES encryption key ### next node ### previous node
	Send the node encryption keys and the first node port to the client.
	'''
        random.shuffle(NODE_PORTS)
	ports = [CLIENT_PORT, NODE_PORTS[0], NODE_PORTS[1], NODE_PORTS[2], DIR_PORT]
	#To nodes
	for i in range(3):
		dir = create_socket()
		dir.connect((HOST, int(ports[i+1])))
		msg = KEYS[len(KEYS)-1-i] + "###" +  ports[i+2] + "###" + ports[i]
		encrypted = AES.encrypt(msg, NODE_KEYS[ports[i+1]])
		dir.send(encrypted)
		dir.close()

	#To client
	dir = create_socket()
	dir.connect((HOST, int(CLIENT_PORT)))
	msg = KEYS[0] + "###" + KEYS[1] + "###" + KEYS[2] + "###" + NODE_PORTS[0]
	encrypted = AES.encrypt(msg, CLIENT_KEY)
	dir.send(encrypted)
	dir.close()

def main():
	'''Main functionality of the directory'''
	client_keyexchange()
	create_keys()
	node_keyexchange()
	time.sleep(1)
	key_distribution()

if __name__ == "__main__":
	main()
