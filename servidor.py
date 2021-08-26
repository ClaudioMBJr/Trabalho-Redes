import socket
import struct
import _thread
import time
HOST = ''              # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta

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

def conectado(con, cliente):
	print("Conectado ao cliente: ", cliente)
	idSensor, tpSensor, vlSensor, nmSensor = myRecv(con)
	print (cliente, idSensor, tpSensor, vlSensor, nmSensor.decode())
	# while True:
	# 	msg = con.recv(1024)
	# 	if not msg: break
	# 	print(cliente, ": ", msg.decode())
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