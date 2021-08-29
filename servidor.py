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

def enviaMensagem(msg):
	for con in listCon:
		con.send(msg.encode('UTF-8'))


def verificaUsuario(usuarioConectado):
	usuarios = pd.read_csv('./usuarios.csv').iloc[:,:].values
	for usuario in usuarios:
		if(usuarioConectado == usuario[0]):
			return True

def baixaMensagensNovas(usuario):
	#retirar o \n se não tiver mensagem
		mensagensNovas = "\n"
		if(dicMensagens != {}):
			for key in dicMensagens:
					if(key == usuario):
						lista = dicMensagens[key].split(" ")
						remetente = lista[0]
						mensagem = ""
						
						for i in (lista[2 :]):
							mensagem += i + " "
							
						mensagensNovas += remetente + " " + mensagem + "\n"
						
		return mensagensNovas

def pegaMensagemSemUsuario(msg):
	list = msg.split(" ")
	msg = ""
	for i in (list[1 :]):
		msg += i + " "
	return msg




def conectado(con, cliente):
	print("Conectado ao cliente: ", cliente)
	usuario = con.recv(1024).decode('UTF-8')
	
	while True:
		if (verificaUsuario(usuario)):
			mensagensNovas = baixaMensagensNovas(usuario)
			#incluir o f!
			print(mensagensNovas)
			con.send(mensagensNovas.encode('UTF-8'))

			#zerar dicionario
			##salvar no banco

			msg = con.recv(1024)
			msg = msg.decode('UTF-8')	
			if not msg: break
			destinatario = msg.split(" ")[0]
			
			if(verificaUsuario(destinatario)):
				if(destinatario in dicMensagens.keys()):
					dicMensagens[destinatario] += "\n" + usuario + " " + pegaMensagemSemUsuario(msg)
				else:
					dicMensagens.update({destinatario : usuario+  " " + msg})

		else:
			break
				

	print("Cliente desconectado: ", cliente)
	_thread.exit()

### Inicio da execucao do programa
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(1)

dicMensagens = {}

while True:
    con, cliente = tcp.accept()
    _thread.start_new_thread(conectado, tuple([con, cliente]))

tcp.close()
