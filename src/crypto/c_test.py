from Crypto.PublicKey import RSA

key = RSA.generate(1024)
print("RSA Key: "+ str(key))
f = open('mykey.pem','w')
f.write(key.exportKey('PEM'))
f.close()
