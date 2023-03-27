import socket
import select
import time
from typing import List

# definindo host e porta
HOST = 'localhost'
PORT = 80

# criando o objeto do socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

print('[°] Servidor Ligado')

print('Aguardando conexões...')

conn_list = [] # type: List[socket.socket]

server.listen() # escuta por novas conexões dos clients


while True:
    readable, writable_not_in_use, exceptions_not_in_use = select.select([server, * conn_list], [], [], 0.016)
    readable = readable # type: List[socket.socket]

    for author in readable:
        if author is server:
            conn, addr = server.accept() # checa se as coisas que estão a ser recebidas são novas conexões e as aceita
            host, port = addr

            timenow = time.strftime('[%H:%M:%S]')
            print(f'{timenow} {host} se  conectou pela porta: {port}')

            conn_list.append(conn)
        else:
            data = author.recv(1024) # checa se as coisas que estão a ser recebidas são mensagens e as guarda na variavel data

            if data:
                for client in conn_list:
                    if client != author:
                        client.sendall(data) # envia as mensagens para todos no servidor exceto para o transmissor da mesma
