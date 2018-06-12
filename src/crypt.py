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
import Crypto.Cipher.AES
import Crypto.Util.Counter


def add_padding(s):
    res = s + ''.join([str(len(s)%16) for i in range(16 - len(s)%16)])
    print("add_padding: "+res)
    return res
    #return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)

def remove_padding(s):
    leng = int(s[-1])
    res = s[:len(s)- (16-leng)]
    print("remove_padding: "+res)
    return res

def int_of_string(s):
    return int(binascii.hexlify(s), 16)
	
def encrypt_message(key, plaintext):
    iv = os.urandom(16)
    plaintext = add_padding(plaintext)
    ctr = Counter.new(128, initial_value=int_of_string(iv))
    #ctr = Crypto.Util.Counter.new(128, initial_value=long(iv.encode("hex"), 16))
    aes = AES.new(key, AES.MODE_CTR, counter=ctr)
    return iv , aes.encrypt(plaintext)
	
def decrypt_message(key, ciphertext, iv):
    ctr = Counter.new(128, initial_value=int_of_string(iv))
    #ctr = Crypto.Util.Counter.new(128, initial_value=long(iv.encode("hex"), 16))
    aes = AES.new(key, AES.MODE_CTR, counter=ctr)
    return remove_padding(aes.decrypt(ciphertext))

