from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Crypto import Random
from base64 import b64encode, b64decode

class Encryption():
    key = None
    hash = SHA512.new()

    def __init__(self, path=None):
        if(path != None):
            f = open(path,'rb')
            self.key = RSA.import_key(f.read())
            print(self.key.exportKey(format='PEM'))
        else:
            random_generator = Random.new().read
            self.key  = RSA.generate(1024, random_generator) #generate pub and priv key

            f = open("./utils/private.pem", "wb")
            f.write(self.key.exportKey('PEM'))
            f.close()

            f = open("./utils/public.pem", "wb")
            f.write(self.key.publickey().exportKey('PEM'))
            f.close()

    def encrypt(self, message, pub_key):
        cipher = PKCS1_OAEP.new(pub_key)
        return cipher.encrypt(message)

    def decrypt(self, message):
        cipher = PKCS1_OAEP.new(self.key)
        return cipher.decrypt(message)

    def sign(self, message):
        signer = PKCS1_v1_5.new(self.key)
        self.hash.update(message)
        return signer.sign(self.hash)

    def verify(self, message, signature, pub_key):
        signer = PKCS1_v1_5.new(pub_key)
        self.hash.update(message)
        return signer.verify(self.hash, signature)

if __name__ == "__main__":
    enc = Encryption(path="./utils/private.pem")
    # enc = Encryption()
