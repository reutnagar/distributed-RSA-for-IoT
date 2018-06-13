#	Asymmetric Encryption/ Decryption
#	With RSA

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

def generate_asym_key(bits=2048):
	# default exponent is: 65537 (0x10001)
	new_key = RSA.generate(bits)
	public_key = new_key.publickey().exportKey("PEM")
	private_key = new_key.exportKey("PEM")
	return public_key, private_key
	
def encrypt_asym(pub_key, message):
	key = RSA.import_key(pub_key)
	cipher = PKCS1_v1_5.new(key)
	ciphertext = cipher.encrypt(message)
	return ciphertext
	
def decrypt_asym(priv_key, ciphertext):
	print("in decrypt_asym #1")
	key = RSA.import_key(priv_key)
	print("in decrypt_asym #2")
	cipher = PKCS1_v1_5.new(key)
	print("in decrypt_asym #3")
	message = cipher.decrypt(ciphertext, None)
	print("in decrypt_asym #4")
	return message


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

