import base64
import random
import string
from Crypto.Cipher import AES

class AES_func:
        def __init__(self):
                self.MODE = AES.MODE_CBC #Cipher-Block Chaining
                self.IV = '\x00' * 16 #Initialization vector for encryption and decryption

        def add_padding(self, text):
                '''
                Input: String
                Output : Same string but length is dividable by 16
                adds % to the string
                '''
                while len(text) % 16 != 0:
                        text += "%"
                return text

        def remove_padding(self, text):
                '''
                Input: String with padding
                Output: String with out padding
                '''
                return text.replace("%", "")

        def DH_keygen(self, key): #Incorrect name, too lazy to change all files
                '''
                Input: Result of Diffie-Hellman key excange
                Output: Encryption key, length is 16
                Adds the letter a to the given number until string len is 16
                '''
                #Creation of truly secure keys
                while len(key) != 16:
                        key += "a"
                return key

        def DF_keygen(self, seed):
                '''
                Input: Seed, result of key exchange
                Output: 16 char long "random" string based on seed
                '''
                random.seed(seed)
                key = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for i in range(16))
                return key

        def encrypt(self, text, key):
                '''
                Input: Text to encrypt, key for DF_keygen
                Output: Encrypted text
                Uses AES encryption to encrypt the string
                '''
                encrypter = AES.new(key, self.MODE, self.IV)
                text = encrypter.encrypt(self.add_padding(text))
                return base64.b64encode(text)

        def decrypt(self, text, key):
                '''
                Input: Encrypted text, key
                Output: Decrypted text
                '''
                decrypter = AES.new(key, self.MODE, self.IV)
                text = base64.b64decode(text)
                text = decrypter.decrypt(text)
                return self.remove_padding(text)