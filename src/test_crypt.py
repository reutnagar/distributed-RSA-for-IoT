# This module tests "crypt.py" functionality
import crypt
import random, string


private, public = crypt.generate_asym_key()
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

KEY_SIZE = 16	
key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(KEY_SIZE))
print("AES key: "+ key)
#cipher = crypt.encrypt_AES(key, MESSAGE)
#print("cipher: "+ str(cipher))