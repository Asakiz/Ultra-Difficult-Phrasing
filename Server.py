import socket
import threading
import sys
import time

class Server:

	def __init__(self, port=10000):
		self.port = port
		

	def sender(self, message, address):
		self.threadfinished = False
		print('debug1 %s', message)
		while(self.threadfinished == False):
			self.sock.sendto(message.encode(), address)
			print('\nsending again..')
			time.sleep(1)

	def listener(self, message):
		print('debug2 %s', message)
		data, address = self.sock.recvfrom(1024)
		while data.decode() != message:
			data, address = self.sock.recvfrom(1024)
		self.threadfinished = True
		self.data = data
		self.address = address
		return

	def waitNewCnx(self):
		self.threadfinished = False
		t1 = threading.Thread(target=self.listener(), args=('NEWCNX',))
		t1.start()
		t1.join()
		self.player1 = self.address
		self.threadfinished = False
		t1 = threading.Thread(target=self.sender(), args=('CNXACK', self.player1))
		t2 = threading.Thread(target=self.listener(), args=('CNXACKACK'))
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
