import tkinter as tk
import socket
import time
import threading

#definindo host e porta
HOST = 'localhost'
PORT = 80

#criando o objeto do socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

print('Servidor ligado [°]')

#aceita novas conexões e captura o ip e a porta
conn, adress = s.accept()
host, port = adress

#cria um aviso no servidor para cada conexão
timenow = time.strftime('[%H:%M:%S]')
print(f'{timenow} {host} se conectou pela porta: {port}')

#função para receber mensagens e printa-las na GUI
def receber_mensagens():
    while True:
        data = conn.recv(1024).decode('utf-8')
        if not data:
            break
        mensagens.configure(state=tk.NORMAL)
        mensagens.insert(tk.END, "Usuário: " + data + "\n")
        mensagens.configure(state=tk.DISABLED)
        mensagens.see(tk.END)

#função para enviar mensagens e printa-las na GUI
def enviar_mensagem(event=None):
    mensagem = caixa_de_texto.get().strip()
    if not mensagem:
        return
    conn.sendall(mensagem.encode('utf-8'))

    mensagens.configure(state=tk.NORMAL)
    mensagens.insert(tk.END, "Você: " + mensagem + "\n")
    mensagens.configure(state=tk.DISABLED)
    caixa_de_texto.delete(0, tk.END)
    mensagens.see(tk.END)

#cria o objeto da GUI
janela = tk.Tk()
janela.title("chatDark")

frame_mensagens = tk.Frame(janela)
frame_mensagens.pack(fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(frame_mensagens)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

mensagens = tk.Text(frame_mensagens, wrap=tk.WORD, yscrollcommand=scrollbar.set)
mensagens.pack(fill=tk.BOTH, expand=True)
scrollbar.config(command=mensagens.yview)
mensagens.configure(state=tk.DISABLED)

frame_envio = tk.Frame(janela)
frame_envio.pack(fill=tk.X, side=tk.BOTTOM)

caixa_de_texto = tk.Entry(frame_envio)
caixa_de_texto.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)
caixa_de_texto.bind('<Return>', enviar_mensagem)

botao_enviar = tk.Button(frame_envio, text="Enviar", command=enviar_mensagem)
botao_enviar.pack(side=tk.RIGHT, padx=5, pady=5)

#coloca o recebimento de mensagens como outra thread
thread = threading.Thread(target=receber_mensagens)
thread.start()

#mantém a GUI em funcionamento
janela.mainloop()
