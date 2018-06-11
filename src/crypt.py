#	Asymmetric Encryption/ Decryption
#	With RSA

from Crypto.PublicKey import RSA

def generate_asym_key(bits=2048):
	# default exponent is: 65537 (0x10001)
	new_key = RSA.generate(bits)
	public_key = new_key.publickey().exportKey("PEM")
	private_key = new_key.exportKey("PEM")
	return private_key, public_key
	
def encrypt_asym(pub_key, message):
	pub = RSA.importKey(pub_key, "PEM")
	cipher = pub.encrypt(message, 32)
	return cipher
	
def decrypt_asym(priv_key, cipher):
	priv = RSA.importKey(priv_key, "PEM")
	message = priv.decrypt(cipher)
	return message

#	Symmetric Encryption/ Decryption
#	With AES

#from Crypto.Cipher import AES

#def encrypt_AES(key, message):
#	stream = AES.new(key, AES.MODE_CTR, 0)
#	cipher = stream.encrypt(message)
#	return cipher

# import base64
# import hashlib
# from Crypto import Random
# from Crypto.Cipher import AES

# class AESCipher(object):

    # def __init__(self, key): 
        # self.bs = 32
        # self.key = hashlib.sha256(key.encode()).digest()

    # def encrypt(self, raw):
        # raw = self._pad(raw)
        # iv = Random.new().read(AES.block_size)
        # cipher = AES.new(self.key, AES.MODE_CBC, iv)
        # return base64.b64encode(iv + cipher.encrypt(raw))

    # def decrypt(self, enc):
        # enc = base64.b64decode(enc)
        # iv = enc[:AES.block_size]
        # cipher = AES.new(self.key, AES.MODE_CBC, iv)
        # return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    # def _pad(self, s):
        # return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)
    # @staticmethod
    # def _unpad(s):
        # return s[:-ord(s[len(s)-1:])]



#	Symmetric Encryption/ Decryption
#	With AES

import binascii
import os
from Crypto.Cipher import AES
from Crypto.Util import Counter

def get_iv():
	return os.urandom(16)

iv = get_iv()

def pad(s):
    return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
    #return s.zfill(16)

def int_of_string(s):
    return int(binascii.hexlify(iv), 16)
	
def encrypt_message(key, plaintext):
    #iv = os.urandom(16)
    #iv = get_iv()
    ctr = Counter.new(256, initial_value=int_of_string(iv))
    #ctr = pad(ctr)
    aes = AES.new(key, AES.MODE_CTR, counter=ctr)
    return iv , aes.encrypt(plaintext)
	
def decrypt_message(key, ciphertext, iv):
    ctr = Counter.new(256, initial_value=int_of_string(iv))
    aes = AES.new(key, AES.MODE_CTR, counter=ctr)
    return aes.decrypt(ciphertext)

