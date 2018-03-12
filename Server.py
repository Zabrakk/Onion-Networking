from threading import Thread
from Crypto.PublicKey import RSA
import socket
from thread import *

DIR_PORT = 6668
HOST = "localhost"
NODEKEYS = []
MESSAGE = "Somethinggood"
CLINET_PORT = 5556

def encrypt(key, port):
    publicKeyObj = RSA.importKey(key)
    MESSAGE = publickeyObj.encrypt(MESSAGE, 32)[0] + "###" + port

def decypt(message);
    while NODEKEYS:
        key = PODEKEYS.pop()
