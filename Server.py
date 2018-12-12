import socket
import threading
import sys
import time

class Server:

	def __init__(self, port=10000):
		self.port = port
		

	
			

	def sendPhrase():
		print('\nfoo')

	def sendCnxAck(self, address):
		self.sock.sendto('CNXACK', address)

	def recCnxAck(self):
		data, address = self.sock.recvfrom(1024)
		print('debug3 %s' % self.threadfinished)
		while data.decode() != 'CNXACKACK':
			print('debug4 %s' % self.threadfinished)
			data, address = self.sock.recvfrom(1024)
		self.threadfinished = True
		self.data = data
		self.address = address
		return

	def listenerNewCnx(self):
		data, address = self.sock.recvfrom(1024)
		while data.decode() != 'NEWCNX':
			data, address = self.sock.recvfrom(1024)
		self.threadfinished = True
		self.data = data
		self.address = address
		return

	def waitNewCnx(self):
		self.threadfinished = False
		t1 = threading.Thread(target=self.listenerNewCnx())
		t1.start()
		t1.join()
		self.player1 = self.address
		self.threadfinished = False
		print('debug1 %s' % self.threadfinished)
		t2 = threading.Thread(target=self.recCnxAck())
		
		t2.start()
		print('debug2 %s' % self.threadfinished)
		while(self.threadfinished == False):
			sendCnxAck(self.player1)
			print('\nsending again..')
			time.sleep(1)
		#copypaste for player2, so cuidar pra nao deixar o mesmo player conectar 2x






	def main(self):
		# Create a TCP/IP socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		# Bind the socket to the port
		server_address = ('localhost', self.port)
		print('starting up on %s port %s' % server_address)
		self.sock.bind(server_address)
		#self.sock.settimeout(1)#Para testes
		self.waitNewCnx()
		playeripaddress, playerport = self.player1
		print('\nplayer 1 connected, IP: %s' % playeripaddress)
		

if __name__ == "__main__":
	sock=Server()
	sock.main()
