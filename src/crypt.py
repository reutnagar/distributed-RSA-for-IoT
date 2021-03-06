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
	key = RSA.import_key(priv_key)
	cipher = PKCS1_v1_5.new(key)
	message = cipher.decrypt(ciphertext, None)
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
    # The last byte of the message will have the last block original size, so recipient will be able to extract the message
    # if last block is full- no padding needed, a full block will be added with the value of zeros.
    res = s + ''.join([chr(len(s)%16) for i in range(16 - len(s)%16)])
    return res

def remove_padding(s):
    # find the last block original size and remove the padding
    lastBlocklen = ord(s[-1])
    res = s[:len(s)- (16-lastBlocklen)]
    return res

def int_of_string(s):
    return int(binascii.hexlify(s), 16)

# encryption
def encrypt_message(key, plaintext):
    iv = os.urandom(16)
    # encryption is done only on block sizes of the message. therefore need to add padding
    plaintext = add_padding(plaintext)
    ctr = Counter.new(128, initial_value=int_of_string(iv))
    aes = AES.new(key, AES.MODE_CTR, counter=ctr)
    return iv , aes.encrypt(plaintext)

# decryption
def decrypt_message(key, ciphertext, iv):
    ctr = Counter.new(128, initial_value=int_of_string(iv))
    aes = AES.new(key, AES.MODE_CTR, counter=ctr)
    msg = remove_padding(aes.decrypt(ciphertext))
    return msg

