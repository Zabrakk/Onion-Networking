from threading import Thread
from Crypto.PublicKey import RSA
import socket
from thread import *
import random

send_keys = []
return_keys = []
sent = []
dir = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dir.bind(('localhost', 6667))
dir.listen(10)

def connection_threads(conn):
        while True:
                data = str(conn.recv(1024))
                if data == "give_send": #Send keys to client
                        conn.send(choose_send_order(send_keys))
                elif data == "give_return": #Send return keys to node
                        conn.send(coohse_order(return_keys))
                elif data.startswith("send_key"): #Get keys from nodes
                        data = data.split("###")
                        send_keys.append(data[1:3])
                elif data.startswith("return_key"):
                        data = data.split("###")
                        return_keys.append(data[1:3])

def choose_send_order(keylist):
        #Generate random order for nodes
        num = random.randint(0, (len(send_keys) - 1))
        keys  = send_keys[num][0] + "###" + send_keys[num][1]
        send_keys.remove(send_keys[num])
        sent.append(keys)
        return keys

def send_return_keys():
        return False

while True:
        conn, addr = dir.accept()
        #print "Connected from: " + addr[0] + ":" + str(addr[1])
        start_new_thread(connection_threads, (conn,))

server.close()
