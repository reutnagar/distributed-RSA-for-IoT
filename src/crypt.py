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

from Crypto.Cipher import AES

#def encrypt_AES(key, message):
#	stream = AES.new(key, AES.MODE_CTR, 0)
#	cipher = stream.encrypt(message)
#	return cipher
