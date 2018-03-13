from threading import Thread
from Crypto.PublicKey import RSA
import socket
from thread import *
import random

DIR_PORT = 6668
HOST = "localhost"
NODEKEYS = []
CLIENT_PORT = 5556
MESSAGE = "sometinggood###" + str(CLIENT_PORT)

def encrypt(key, port):
        publickeyObj = RSA,importKey(key)
        MESSAGE = publickeyObj.encrypt(MESSAGE, 32)[0] + "###" + str(CLIENT_PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((HOST, DIR_PORT))
while len(NODEKEYS) < 3:
        server.send("sendreturn")
        message = server.recv(1024)
        print(message)
        key, port = str(message).split("###")
        #encyptt(key, port)
        NODEKEYS.append(key)

print NODEKEYS
server.close()
