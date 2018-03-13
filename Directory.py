from threading import Thread
from Crypto.PublicKey import RSA
import socket
from thread import *
import random

new_key = RSA.generate(1024)
send_keys = []
return_keys = []

def choose_order():
        if  action == "send":
                num = random.randint(0, (len(send_keys) - 1))
                keys = send_keys[num][0] + "###" + send_keys[num][1]
                send_keys.remove(send_keys[num])
        elif action == "return":
                num = random.randint(0, (len(return_keys) -1))
                keys = return_keys[num][0] + "###" + return_keys[num][1]
                return_keys.remove(return_keys[num])
        print keys
        return keys


def client_thread(conn):
        while True:
                data = str(conn.recv(1024))
                if str(data) == "gimmekeys":
                        conn.send(choose_order("send"))
                elif str(data) == "sendreturn":
                        conn.send(choose_order("return"))
                elif data.startswith("sendkeys"):
                        data = data.split("###")
                        send_keys.append(data[1:3])
                elif data.startswith("returnkeys"):
                        data = data.split("###")
                        return_keys.append(data[1:3])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 6668))
server.listen(5)

while 1:
        conn, addr = server.accept()
        print 'Connected from: ' + addr[0] + ':' + str(addr[1])
        start_new_thread(client_thread, (conn,))

server.close()
