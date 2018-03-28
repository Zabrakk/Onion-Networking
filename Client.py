from Crypto.PublicKey import RSA
import socket
from thread import *
from Crypto.Cipher import AES

DIR_PORT = 6667
CLIENT_PORT = 6660
HOST = "localhost"
keys = []
message = "Hello worldddddd###6789" #Number is servers port
#Message must be 16bit for PyCrypto AES

#Ei turvallista
key = 'a' * 16
IV = 16 * '\x00'
mode = AES.MODE_CBC
encryptor = AES.new(key, mode, IV=IV)

def encrypt_message(): #Asymmetric for fowarding
        for i in range(len(keys)):
                key = RSA.importKey(keys[i][0])
                encrypted_message = str(key.encrypt(message, 32)) + "###" + keys[i][1]
        print encrypted_message
        return encrypted_message

def decrypt_message(message): #Symmetric key for return
        decryptor = AES.new(key, mode, IV=IV)
        return str(decryptor.decrypt(message))

def send_key():
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, DIR_PORT))
        client.send("return_key###" + public_key + "###" + str(CLIENT_PORT))
        print("Sending key to directory")
        client.close()

def get_keys():
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, DIR_PORT))
        while len(keys) < 3:
                client.send("give_send")
                data = str(client.recv(1024))
                key, port = data.split("###")
                keys.append([key, port])


#encrypt_message()
#print public_key
#print private_key
#send_key()
get_keys()

print decrypt_message(encryptor.encrypt(message[0:16]))
