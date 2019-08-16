import socket
from threading import Thread

HOST = "localhost"

class Server:
	def __init__(self,port,page_name,answer):
		self.PORT = port #Server port
		self.PAGE_NAME = page_name #Which "website" the server is
		self.ANSWER = answer #Predetermined answer the server gives to its client

	def create_socket(self):
		'''Creates sockets'''
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		return server

	def server_listen(self):
		'''Does what the server is supposed to do'''
		server = self.create_socket()
		server.bind((HOST, self.PORT))
		server.listen(1)
		conn, addr = server.accept()
		msg = str(conn.recv(1024))
		if msg == self.PAGE_NAME: #If client asked the right page
			conn.send(self.ANSWER.encode('utf-8'))
		else: #If it was something else
			conn.send('404 Not Found'.encode('utf-8'))

	def main(self):
		self.server_listen()



ports = [7777, 7788, 7799]
sites = ['youtube.com', 'vauva.fi', 'memecenter.com']
answers = ['This is youtube', 'This is troll forum', 'This is Sparta']
for i in range(3):
	Thread(target = Server(ports[i],sites[i],answers[i]).main).start()

