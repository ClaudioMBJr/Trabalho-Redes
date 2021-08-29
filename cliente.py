#SALVE
import socket
import struct
import pandas as pd

HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 3333            # Porta que o Servidor esta
# Campos da mensagem
idSensor = 2		# inteiro de 4 bytes sem sinal
tpSensor = 6		# inteiro de 2 bytes sem sinal
vlSensor = 32			# inteiro de 2 bytes
nmSensor = "Sensor de presença"  #Ate 20 bytes
structsize = 28			# quantidade de bytes da mensagem

# Funcao de empacotamento e envio de da mensagem
def mySend (socket, idSensor, tpSensor, vlSensor):
	msg = struct.pack('!IHh20s', idSensor, tpSensor, vlSensor, nmSensor.encode())
	print (msg)
	socket.send (msg)

def mostraMensagens():
	msg = tcp.recv(1024)
	msg = msg.decode('UTF-8')
	print(msg)

######### Inicio do programa
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)

######### Envia uma mensagem
# mySend (tcp, idSensor, tpSensor, vlSensor)
print ('Para sair use CTRL+X\n')
msg = input("Digite o nome do usuário: ")
tcp.send (msg.encode())
while msg != '\x18':
	msg = tcp.recv(1024)
	msg = msg.decode('UTF-8')
	print(msg)
	if msg == "Usuário inválido":
		print("Você foi desconectado!")
		break
	msg = input("Digite uma mensagem: ")
	tcp.send (msg.encode())
	

tcp.close()