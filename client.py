import socket

HOST = 'localhost'
PORT = 80

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    data = s.recv(1024).decode('utf-8')

    if data:
        print(data)
