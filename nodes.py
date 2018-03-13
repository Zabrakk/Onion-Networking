import socket
from Crypto.PublicKey import RSA
from threading import Thread
from base64 import b64decode

DIRPORT = 6668
ports = [6555, 6444, 6333]

class Node:
        def __init__(self, host, port):
                self.node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.node.bind((host, port))
                self.node.listen(10)
                self.publickey = ""
                self.privatekey = ""
                self.port = port
                
        def make_keys(self):
                new_sendkey = RSA.generate(1024)
                new_returnkey = RSA.generate(1024)
                self.send_publickey = new_sendkey.publickey().exportKey('PEM')
                self.send_privatekey = new_sendkey.exportKey('PEM')
                self.return_publickey = new_returnkey.publickey().exportKey('PEM')
                self.return_privatekey = new_returnkey.exportKey('PEM')

         def decrypt(self, message):
                raw_data = b64decode(message)
                decrypted = self.return_key.decrypt(raw_data)
                print decrypted
                return decypted

                
        def send_key_port(self):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(('localhost', DIRPORT))
                s.send("sendkeys###" + self.send_publickey + "###" + str(self.port))
                print("sending send keys")
                s.close()
                
        def return_key(self):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(('localhost', DIRPORT))
                s.send("returnkeys###" + self.return_publickey + "###" + str(self.port))
                print "sending return keys"
                s.close()



        def mainloop(self):
                self.make_keys()
                self.send_key_port()
                self.return_key()
                #while True:
                #       conn, addr = self.node.accept()
                #       print("Connected with " + addr[0] + " : " + str(addr[1]))
                
for i in range(3):
        Thread(target = Node('localhost', ports[i]).mainloop).start()
#Thread(target = Node('localhost', 6444).mainloop).start()
#Thread(target = Node('localhost', 6333).mainloop).start()
