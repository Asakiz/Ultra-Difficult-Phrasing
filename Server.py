import socket
import threading
import sys
import time

class Server:

	def __init__(self, port=10000):
		self.port = port
		

	def sender(self):
		self.threadfinished = False
		print('debug1 %s', self.msgsender)
		while(self.threadfinished == False):
			self.sock.sendto(self.msgsender.encode(), self.addrsender)
			print('\nsending again..')
			time.sleep(1)

	def listener(self):
		print('debug2 %s', self.msglistener)
		data, address = self.sock.recvfrom(1024)
		while data.decode() != self.msglistener:
			data, address = self.sock.recvfrom(1024)
		self.threadfinished = True
		self.data = data
		self.address = address
		return

	def waitNewCnx(self):
		self.threadfinished = False
		self.msglistener = 'NEWCNX'
		t1 = threading.Thread(target=self.listener())
		t1.start()
		t1.join()
		self.player1 = self.address
		self.threadfinished = False
		self.msgsender = 'CNXACK'
		self.addrsender = self.player1
		t1 = threading.Thread(target=self.sender())
		self.msglistener = 'CNXACKACK'
		t2 = threading.Thread(target=self.listener())
		t1.start()
		t2.start()
		t1.join()
		t2k.join()
		
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
