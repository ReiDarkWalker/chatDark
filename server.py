import socket
import threading
import time

#definindo host e porta
HOST = 'localhost'
PORT = 80

#criando o objeto do socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(2) #espera por até 2 conexões (dois clients)

print('[°] Servidor Ligado')

print('Aguardando conexões...')

#cria o objeto socket do primeiro client, captura seu ip e cria um log no servidor de conexão
client_conn1, client_address1 = s.accept()
host, port = client_address1
timenow = time.strftime('[%H:%M:%S]')
print(f'{timenow} {host} se conectou pela porta: {port}')

#cria o objeto socket do segundo client, captura seu ip e cria um log no servidor de conexão
client_conn2 ,client_address2 = s.accept()
host, port = client_address2
timenow = time.strftime('[%H:%M:%S]')
print(f'{timenow} {host} se conectou pela porta: {port}')

while True:
    
    def envio1(): #recebe o que o primeiro client envia, checa se ele está enviando algo, se sim, o envia para o segundo client
        data_c1 = client_conn1.recv(1024) 
        if data_c1:
            client_conn2.sendall(data_c1)

    def envio2(): #recebe o que o segundo client envia, checa se ele está enviando algo, se sim, o envia para o primeiro client
        data_c2 = client_conn2.recv(1024)
        if data_c2:
            client_conn1.sendall(data_c2)

    #coloca os 2 envios em threads separadas para poderem enviar normalmente sem limitações
    threading.Thread(target=envio1).start()
    threading.Thread(target=envio2).start()
