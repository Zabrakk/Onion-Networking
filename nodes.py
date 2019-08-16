import socket
import time
from diffiesecret import *
from AES_func import AES_func
from threading import Thread
from random import randint

#Connection config
HOST = "localhost"
DIR_PORT = 6677 #Directories port
NODES = [] #List of nodes

#Functions in the node class are called in the order they are presented in the code
#except for loop()

class Node:
	def __init__(self): #Initialization of the node object
		print("Node starting")
		self.AES = AES_func()
		self.SECRET = randint(1, 100)
		self.DIR_KEY = 0
		self.COMM_KEY = 0
		self.PORT = 0
		self.PREV_PORT = 0
		self.NEXT_PORT = 0
		self.DIR_exchange()

	def create_socket(self):
		'''Look at the other files :) '''
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		return sock

	def DIR_exchange(self):
		'''
		Input: None
		Output: None
		Perfoms DH key exchange, creates an AES key with DH result
		Uses the key to decrypt the other part of the message containing the nodes port
		'''
		sock = self.create_socket()
		sock.connect((HOST, DIR_PORT))

		sock.send(calculate_shared(self.SECRET).encode("utf-8"))
		answer = sock.recv(1024).split("###")
		self.DIR_KEY = calculate_secret(answer[0], self.SECRET)
		self.DIR_KEY = self.AES.DF_keygen(self.DIR_KEY)
		self.PORT = int(self.AES.decrypt(answer[1], self.DIR_KEY))
		print(self.DIR_KEY) #Debug prints
		print(self.PORT)
		sock.close()

	def get_comm_key(self):
		'''
		Input: None
		Output: None
		Connects to directory, recieves return and fowarding ports and an AES key used for communication
		between nodes, client and server
		'''
		sock = self.create_socket()
		sock.bind((HOST, self.PORT))
		sock.listen(2) #1
		conn, addr = sock.accept()

		answer = self.AES.decrypt(conn.recv(1024), self.DIR_KEY) #Encryption key, to, from
		self.COMM_KEY, self.NEXT_PORT, self.PREV_PORT = answer.split("###")
		print(self.COMM_KEY, self.NEXT_PORT, self.PORT, self.PREV_PORT)

	def listener(self):
		'''
		Input: None
		Output: None
		Fowarding and returnin the message
		Does encryption and decryption based on message direction
		'''
		server = self.create_socket()
		server.bind((HOST, self.PORT))
		server.listen(3)
		conn, addr = server.accept()
		msg = self.AES.decrypt(conn.recv(1024), self.COMM_KEY).split("###")
		print(msg)
		time.sleep(1)
		client = self.create_socket()
		if len(msg) == 1:
			client.connect((HOST, int(self.NEXT_PORT)))
		else:
			client.connect((HOST, int(msg[len(msg)-1])))
		client.send(msg[0].encode('utf-8'))
		answer = self.AES.encrypt(client.recv(1024),self.COMM_KEY)
		client.close()
		conn.send(answer.encode('utf-8'))

	def main(self):
		self.get_comm_key()
		self.listener()

for i in range(3): #Start 3 nodes
	Thread(target = Node().main).start()
