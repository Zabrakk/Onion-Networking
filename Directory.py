from threading import Thread
from Crypto.PublicKey import RSA
import socket
from thread import *

new_key = RSA.generate(1024)
servers = []

def tostr(servers):
        keys = ""
        for o in range(len(servers)):
                for i in range(len(servers[o])):
                        keys += servers[o][i] + "###"
        return keys

def client_thread(conn):
        #conn.send("Do you want keys?")
        while True:
                data = str(conn.recv(1024))
                if str(data) == "gimmekeys":
                        conn.send(tostr(servers))
                elif data.startswith("onionnode"):
                        print("Yhhdddssttyyy")
                        data = data.split("###")
                        servers.append(data[1:3])
                        print(servers)
                #conn.send(keylist['Client'].exportKey('PEM'))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 6668))
server.listen(4)

print(tostr(servers))

while 1:
        conn, addr = server.accept()
        print 'Connected from: ' + addr[0] + ':' + str(addr[1])
        start_new_thread(client_thread, (conn,))

server.close()

