from threading import Thread
from Crypto.PublicKey import RSA
import socket
from thread import *
import random

"""keylist = {
        'Client': RSA.generate(1024),
        'Server1': RSA.generate(1024),
        'Server2': RSA.generate(1024),
        'Public_key': RSA.generate(1024)
        }"""

new_key = RSA.generate(1024)
servers = []

def choose_order():
        num = random.randint(0, (len(servers) - 1))
        keys = servers[num][0] + "###" + servers[num][1]
        servers.remove(servers[num])
        print keys
        return keys

def client_thread(conn):
        while True:
                data = str(conn.recv(1024))
                if str(data) == "gimmekeys":
                        conn.send(choose_order())
                elif data.startswith("onionnode"):
                        data = data.split("###")
                        servers.append(data[1:3])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 6668))
server.listen(4)

while 1:
        conn, addr = server.accept()
        print 'Connected from: ' + addr[0] + ':' + str(addr[1])
        start_new_thread(client_thread, (conn,))

server.close()
