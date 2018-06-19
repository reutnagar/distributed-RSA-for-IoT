# This module tests "crypt.py" functionality
import os
import sys

from .. import crypt
import random, string

#RSA testing
public, private = crypt.generate_asym_key()
print("private key: " + str(private))
print("public key: " + str(public))

MESSAGE = "This Is Secret!"
cipher = crypt.encrypt_asym(public, MESSAGE)
print("cipher: "+ str(cipher))

message_decrypted = crypt.decrypt_asym(private, cipher)
print("message_decrypted: " + str(message_decrypted))

if(message_decrypted != MESSAGE):
	print("Test Failed! The decrypted message is different than the encrypted message!")
else:
	print("Test Passed!")

#AES testing
KEY_SIZE = 16	
key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(KEY_SIZE))
print("AES key: "+ key)

msg = "This is a very secret message from: 10.0.0.24"
iv, cipher = crypt.encrypt_message(key, msg)
print("cipher: "+ str(cipher))

message_decrypted = crypt.decrypt_message(key, cipher, iv)#crypt.get_iv())
print("message_decrypted: " + str(message_decrypted))

if(message_decrypted != msg):
	print("Test Failed! The decrypted message is different than the encrypted message!")
else:
	print("Test Passed!")
	
#cipher = crypt.encrypt_AES(key, MESSAGE)
#print("cipher: "+ str(cipher))
# c = crypt.AESCipher(key)
# msg = "it's a msg tocheck the AES"
# cipher = c.encrypt(msg)
# print("cipher: "+ str(cipher))
# print(len(cipher))

# message_decrypted = c.decrypt(cipher)
# if(message_decrypted != msg):
	# print("Test Failed! The decrypted message is different than the encrypted message!")
# else:
	# print("Test Passed!")


	