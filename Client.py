import socket
import threading
from AES_func import AES_func
from diffiesecret import *
from Crypto.Cipher import AES

#Connection config
HOST = "localhost"
DIR_PORT = 6677 #Directories port, connect here
CLIENT_PORT = 6600 #Client own port
NODE_PORT = 0 #Init this variable

#DH
OWNSECRET = 15 #Secret number for Diffie-Hellman

#AES
AES = AES_func() #Create AES_func object for encryption/decryption
DIR_KEY = 0 #Init this variable
KEYS = [] #Last node, ..., first node

PAGES = ["youtube.com", "memecenter.com", "vauva.fi"] #"Websites" we can connect to
SERVER_PORTS = ["7777", "7799", "7788"] #And their ports

def create_socket():
	'''
	Input: None
	Output: Socket
	For creating sockets
	'''
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	return sock

def dir_connect():
	'''
	Input: None
	Output: None
	Connects to the directory to get a encryption key by performing the DH key exchange
	'''

	global DIR_KEY
	print("#: Connecting to directory")
	sock = create_socket()
	sock.connect((HOST, DIR_PORT))

	#DH
	sock.send(calculate_shared(OWNSECRET).encode("utf-8"))
	SECRET = calculate_secret(sock.recv(1024), OWNSECRET)
	print(SECRET)

	DIR_KEY = AES.DF_keygen(SECRET)
	print(DIR_KEY)
	sock.close()

def recieve_keys():
	'''
	Input: None
	Output: None
	Recieves AES keys that the nodes use and the first nodes port
	'''
	global NODE_PORT, KEYS
	sock = create_socket()
	sock.bind((HOST, CLIENT_PORT))
	sock.listen(2)
	conn, addr = sock.accept()

	message = conn.recv(1024) #key0, key1, key2, node_port
	message = AES.decrypt(message, DIR_KEY).split("###")
	KEYS = [message[i] for i in range(3)]
	NODE_PORT = message[3]
	print(KEYS, NODE_PORT)

def select_page():
	'''
	Input: None
	Output: A tuple containing chosen page and its port
	Loops until user enters a suitable option
	'''
	opt = 0
	try:
		while int(opt) not in [1,2,3]:
			opt = raw_input("Choose page, 1: Youtube, 2: Memecenter, 3: Vauva.fi: ")
			return PAGES[int(opt) - 1], SERVER_PORTS[int(opt) - 1]
	except:
		print("Enter a valid number")
		select_page()


def encrypt_msg(target):
	'''
	Input: Clients message, in this case the tuple obtained from select_page
	Output: Encrypted message that is sent to the first node
	Uses each key ones to encrypt the message
	Adds ### betweem the tuples object, plaint text messages split from those
	'''
	msg = target[0] + "###" + target[1]
	for key in KEYS:
		#print(msg)
		msg = AES.encrypt(msg, key)
	print(msg)
	return msg

def decrypt_msg(msg):
	'''
	Input: Message from server
	Output: Decrypted message
	Uses each node key in a reversed order to decrypt the message
	'''
	for key in reversed(KEYS):
		msg = AES.decrypt(msg, key)
	print(msg)

def send_msg_to_node(msg):
	'''
	Input: Encrypted message
	Output: None
	Send the message to first node
	'''
	sock = create_socket()
	sock.connect((HOST, int(NODE_PORT)))
	sock.send(msg.encode("utf-8"))
	return sock.recv(1024).decode("utf-8")
	#sock.close()

def main():
	'''
	Calls each function in order, thats all
	'''
	dir_connect()
	recieve_keys()
	target = select_page()
	msg = encrypt_msg(target)
	answer = send_msg_to_node(msg)
	decrypt_msg(answer)

if __name__ == "__main__": #Start
	main()
