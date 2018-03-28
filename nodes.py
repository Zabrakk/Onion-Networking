import socket
from Crypto.PublicKey import RSA
from threading import Thread
from Crypto.Cipher import AES
import random
import string

DIRPORT = 6667
ports = [6555, 6444, 6333]

class Node:
        def __init__(self, host, port):
                self.node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.node.bind((host, port))
                self.node.listen(10)
                self.send_publickey = ""
                self.port = port
                #AES
                self.key = random.choice(string.letters) * 16
                self.IV = 16 * '\x00'
                self.mode = AES.MODE_CBC
                self.encryptor = AES.new(self.key, self.mode, IV=self.IV)

        def make_keys(self):
                new_sendkey = RSA.generate(1024)
                new_returnkey = RSA.generate(1024)
                self.send_publickey = new_sendkey.publickey().exportKey('PEM')
                self.send_privatekey = new_sendkey.exportKey('PEM')
                self.return_publickey = new_returnkey.publickey().exportKey('PEM')
                self.return_privatekey = new_returnkey.exportKey('PEM')

        def decrypt(self, message):
                decryptor = AES.new(self.key, self.mode, IV=self.IV)
                return str(decryptor.decrypt(message))

        def send_key_port(self):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(('localhost', DIRPORT))
                s.send("send_key###" + self.send_publickey + "###" + str(self.port))
                print("sending send keys")
                s.close()

        def return_key(self):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(('localhost', DIRPORT))
                s.send("return_key###" + self.return_publickey + "###" + str(self.port))


        def mainloop(self):
                self.make_keys()
                self.send_key_port()
                #self.return_key()
                #while True:
                #       conn, addr = self.node.accept()
                #       print("Connected with " + addr[0] + " : " + str(addr[1]))

for i in range(3):
        Thread(target = Node('localhost', ports[i]).mainloop).start()
