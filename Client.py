from Crypto.PublicKey import RSA
import socket
from thread import *
from Crypto.Cipher import AES
import random
import string

DIR_PORT = 6667
CLIENT_PORT = 6660
HOST = "localhost"
keys = []
return_keys = []
send_data = []
message = "Hello worldddddd###6789" #Number is servers port
#Message must be 16bit for PyCrypto AES

#Ei turvallista
key = 'a' * 16
IV = 16 * '\x00'
mode = AES.MODE_CBC
encryptor = AES.new(key, mode, IV=IV)

def encrypt_message(): #Asymmetric keys for fowarding
        key = RSA.importKey(keys[0][0])
        first_encrypt = str(key.encrypt(message, 32)) + "###" + return_keys[0][0] + "###" + return_keys[0][1] + "###" + str(return_keys[0][2])+ "###"  + keys[0][1]
        second_encrypt = str(key.encrypt(first_encrypt, 32)) + "###" + return_keys[1][0] + "###" + return_keys[1][1]+ "###" + str(return_keys[1][2]) + "###" + keys[1][1]
        third_encrypt = str(key.encrypt(second_encrypt, 32)) +  "###" + return_keys[2][0] + "###" + return_keys[2][1]+ "###" + str(return_keys[2][2]) + "###" + keys[2][1]
        print third_encrypt
        split_encrypted(third_encrypt)
        #for i in range(1, len(keys)):
        #       key = RSA.importKey(keys[i][0])
        #       encrypted_message += str(key.encrypt(encrypted_message, 32)) + "###" + keys[i][1] +  "###" + return_keys[i][0] + "###" + return_keys[i][1]+ "###" + str(return_keys[i][2])
        #       print encrypted_message
        #       print
        #return encrypted_message

def create_return(): #Seeds for node keys
        for i in range(3):
                key = random.choice(string.letters) * 16
                print key
                IV = 16 * '\x00'
                mode = AES.MODE_CBC
                return_keys.append([key, IV, mode])
                print return_keys
        print

def split_encrypted(encrypted): #Port, char*16, IV, AES.mode.
        print str(encrypted).split("###")
        data = encrypted.split("###")
        send_data.append(data[1:])
        print
        print send_data
        send_message(encrypted, send_data)

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

def send_message(message, data):
        #client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #client.connect((HOST, data[0]))
        #client.send(message)
        print message[:-7]

get_keys()
create_return()
encrypt_message()
#print public_key
#print private_key
#send_key()


print decrypt_message(encryptor.encrypt(message[0:16]))
