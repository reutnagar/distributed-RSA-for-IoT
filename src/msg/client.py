import socket

host = '10.0.0.1'
port = 50004

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
print("Connected to "+(host)+" on port "+str(port))
initialMessage = raw_input("Send: ")
s.sendall(initialMessage)

while True:
 data = s.recv(1024)
 print("Recieved: "+(data))
 response = raw_input("Reply: ")
 if response == "exit":
     break
 s.sendall(response)
s.close()

#the server.py

# import socket

# host = '10.0.0.1'
# port = 50001

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((host, port))
# s.listen(1)
# conn, addr = s.accept()
# print ("Connection from", addr)
# while True:
#     data = conn.recv(1024)
#     if not data: break
#     print("Recieved: "+(data))
#     response = raw_input("Reply: ")
#     if response == "exit":
#         break
#     conn.sendall(response)
# conn.close()