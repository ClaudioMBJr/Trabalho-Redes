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

# Funcao de recepcao e desempacotamento da mensagem
def myRecv (socket):
	try:
		msg = socket.recv(structsize)
		print (cliente, msg)
		return struct.unpack('!IHh20s', msg)
	except:
		return None

def verificaUsuario(usuarioConectado):
	usuarios = pd.read_csv('./usuarios.csv').iloc[:,:].values
	for usuario in usuarios:
		if(usuarioConectado == usuario[0]):
			return True

def baixaMensagens(usuario):
	mensagens = pd.read_csv('./mensagem.csv').iloc[:,:].values
	mensagensDoUsuario = "Novas mensagens: \n"
	for mensagem in mensagens:
		if(usuario == mensagem[0]):
			mensagensDoUsuario += mensagem[1] + "\n"
	return mensagensDoUsuario

def conectado(con, cliente):
	print("Conectado ao cliente: ", cliente)
	#idSensor, tpSensor, vlSensor, nmSensor = myRecv(con)
	#print (cliente, idSensor, tpSensor, vlSensor, nmSensor.decode())
	while True:
		msg = con.recv(1024)
		msg = msg.decode('UTF-8')	# Decodifica a mensagem
		if not msg: break
		if(verificaUsuario(msg)):
			print("Usuário conectado: ", msg)
			mensagens = baixaMensagens(msg)
			con.send(mensagens.encode('UTF-8'))
		else:
			print("Usuário não cadastrado: ", msg)
			break

		msg = con.recv(1024)
		msg = msg.decode('UTF-8')	# Decodifica a mensagem
		if not msg: break
		usuario = msg.split(" ")[0]
		
		if(verificaUsuario(usuario)):
			con.send(msg.encode('UTF-8'))
			



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