import tkinter as tk
import socket
import ssl
import threading

#define o host e a porta
HOST = 'localhost'
PORT = 80

#cria o objeto do socket e se conecta ao servidor
sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#cria o objeto do socket como uma conexão segura e criptografada utilizando da biblioteca ssl
context = ssl.create_default_context()
ssl_client = context.wrap_socket(sock_client, server_side = False)

ssl_client.connect((HOST, PORT))

#cria a função de receber mensagens
def receber_mensagem():
    while True:
        data = ssl_client.recv(1024).decode('utf-8')
        
        if not data:
            break

        mensagens.configure(state=tk.NORMAL)
        mensagens.insert(tk.END, "Usuário: " + data + "\n")
        mensagens.configure(state=tk.DISABLED)
        mensagens.see(tk.END)

#cria a função de enviar mensagens
def enviar_mensagem(event=None):
    mensagem = caixa_de_texto.get().strip()

    if not mensagem:
        return
    
    ssl_client.sendall(mensagem.encode('utf-8'))
    
    mensagens.configure(state=tk.NORMAL)
    mensagens.insert(tk.END, "Você: " + mensagem + "\n")
    mensagens.configure(state=tk.DISABLED)
    caixa_de_texto.delete(0, tk.END)
    mensagens.see(tk.END)

#cria a GUI
janela = tk.Tk()
janela.title("Bate-papo")

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

#mantem a função de receber mensagens funcionando em uma thread separada
thread = threading.Thread(target=receber_mensagem)
thread.start()

#mantem a GUI em funcionamento
janela.mainloop()
