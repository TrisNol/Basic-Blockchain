from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Crypto import Random

from base64 import b64decode,b64encode

class Encryption:
    key = None
    hash = SHA512.new()
    temp = None

    def __init__(self, path=None):
        if(path != None):
            f = open(path,'rb')
            self.key = RSA.import_key(f.read())

        else:
            random_generator = Random.new().read
            self.key  = RSA.generate(2048, random_generator) #generate pub and priv key

            f = open("./utils/private.pem", "wb")
            f.write(self.key.exportKey('PEM'))
            f.close()

            f = open("./utils/public.pem", "wb")
            f.write(self.key.publickey().exportKey('PEM'))
            f.close()

    def encrypt(self, message, pub_key):
        pub_key = RSA.importKey(pub_key)
        cipher = PKCS1_OAEP.new(pub_key)
        
        message = cipher.encrypt(message.encode())
        message = str(message)[2:-1]
        return message

    def decrypt(self, message):
        cipher = PKCS1_OAEP.new(self.key)
        message = message.encode().decode('unicode-escape').encode('ISO-8859-1')
        
        message = cipher.decrypt(message)
        message = str(message)[2:-1]
        return message

    def sign(self, message):
        signer = PKCS1_v1_5.new(self.key)
        self.hash.update(message.encode())
        return str(signer.sign(self.hash))

    def verify(self, message, signature, pub_key):

        signer = PKCS1_v1_5.new(pub_key)
        self.hash.update(message)
        return signer.verify(self.hash, signature)
