import socket
import struct
import _thread
import time
import random
import json
import pandas as pd
HOST = ''              # Endereco IP do Servidor
PORT = 3333            # Porta que o Servidor esta

# Campos da mensagem
idSensor = None
tpSensor = None
vlSensor = None
nmSensor = None
structsize = 28

#Dicionario clientes
listCon = []
dicMensagens = {}

def enviaMensagem(msg):
	for con in listCon:
		con.send(msg.encode('UTF-8'))


def verificaUsuario(usuarioConectado):
	usuarios = pd.read_csv('./usuarios.csv').iloc[:,:].values
	for usuario in usuarios:
		if(usuarioConectado == usuario[0]):
			return True

def baixaMensagensNovas(usuario):
	mensagensNovas = " "
	print(dicMensagens)
	if(dicMensagens != {}):
	 	for key in dicMensagens:
	 			if(key == usuario):
	 				mensagensNovas += dicMensagens[key] + "\n"
	return mensagensNovas



def conectado(con, cliente):
	print("Conectado ao cliente: ", cliente)
	usuario = con.recv(1024).decode('UTF-8')
	
	while True:
		if (verificaUsuario(usuario)):
			mensagensNovas = baixaMensagensNovas(usuario)
			#incluir o f
			print(mensagensNovas)
			con.send(mensagensNovas.encode('UTF-8'))

			dicMensagens = {}
			##salva no banco

			msg = con.recv(1024)
			msg = msg.decode('UTF-8')	
			if not msg: break
			destinatario = msg.split(" ")[0]
			
			if(verificaUsuario(destinatario)):
				if(destinatario in dicMensagens.keys()):
					dicMensagens[destinatario] += "\n" + msg
				else:
					dicMensagens.update({destinatario : msg})

		else:
			break
				

	print("Cliente desconectado: ", cliente)
	_thread.exit()

### Inicio da execucao do programa
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(1)

while True:
    con, cliente = tcp.accept()
    _thread.start_new_thread(conectado, tuple([con, cliente]))

tcp.close()
