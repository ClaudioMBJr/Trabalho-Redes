#SALVE
import socket
import struct

HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
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

######### Inicio do programa
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)

######### Envia uma mensagem
mySend (tcp, idSensor, tpSensor, vlSensor)
# print ('Para sair use CTRL+X\n')
# msg = input("Digite uma mensagem: ")
# while msg != '\x18':
# 	tcp.send (msg.encode())
# 	msg = input("Digite uma mensagem: ")

tcp.close()