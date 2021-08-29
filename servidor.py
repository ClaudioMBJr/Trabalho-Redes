import socket
import struct
import _thread
import time
import random
import json
import pandas as pd
import csv
HOST = ''              # Endereco IP do Servidor
PORT = 3333            # Porta que o Servidor esta

# Campos da mensagem
idSensor = None
tpSensor = None
vlSensor = None
nmSensor = None
structsize = 28

#Dicionario clientes



def verificaUsuario(usuarioConectado):
	usuarios = pd.read_csv('./usuarios.csv').iloc[:,:].values
	for usuario in usuarios:
		if(usuarioConectado == usuario[0]):
			return True

def baixaMensagensNovas(usuario):
		mensagensNovas = " "
		chave = " "
		if(dicMensagens != {}):
			for key in dicMensagens:
					if(key == usuario):
						chave = key
						lista = dicMensagens[key].split(" ")
						remetente = lista[0]
						mensagem = ""
						
						for i in (lista[2 :]):
							mensagem += i + " "
							
						mensagensNovas += remetente + ": " + mensagem + "\n" + "f" + "\n"
		
		##########
		if chave != " ":
			deletaChave(chave, dicMensagens)
		return mensagensNovas



def pegaMensagemSemUsuario(msg):
	list = msg.split(" ")
	msg = ""
	for i in (list[1 :]):
		msg += i + " "
	return msg


def deletaChave(chave,dic):
	if dic[chave] != " ":
		del dic[chave]

def salvaNoCSV(mensagem):
	with open('mensagem.csv','w',newline = '') as csvfile:
		writer = csv.writer(csvfile, delimiter = ' ')
		writer.writerow(mensagem)
	

def conectado(con, cliente):
	print("Conectado ao cliente: ", cliente)
	usuario = con.recv(1024).decode('UTF-8')
	destinatario = " "
	
	while True:
		if (verificaUsuario(usuario)):
			mensagensNovas = baixaMensagensNovas(usuario)
			#incluir o f! CHECK
			print(mensagensNovas)
			con.send(mensagensNovas.encode('UTF-8'))

			salvaNoCSV(mensagensNovas)

			
			##salvar no banco 

			msg = con.recv(1024)
			msg = msg.decode('UTF-8')	
			if not msg: break
			destinatario = msg.split(" ")[0]
			
			if(verificaUsuario(destinatario)):
				if(destinatario in dicMensagens.keys()):
					dicMensagens[destinatario] += "\n" + usuario + ": " + pegaMensagemSemUsuario(msg)
				else:
					dicMensagens.update({destinatario : usuario+  " " + msg})

		else:
			con.send('Usuário inválido'.encode('UTF-8'))
			break
				

	print("Cliente desconectado: ", cliente)
	_thread.exit()
	tcp.close()

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
