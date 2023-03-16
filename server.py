import os
import socket

HOST = 'localhost'
PORT = 80

os.system('cls')
print('ligando o servidor...')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

while True:
    s.listen()
    print('Servidor ligado [°]')

    conn, address = s.accept()
    ip, porta = address
    
    if conn:
        print(f'conectaram-se como IP: {ip}, pela porta: {porta}')

    def message():
        while True:
            message = input('mensagem: ')
            packet = message.encode()
            conn.sendall(packet)

    message()
