import socket
import threading
import sys
import time

class Server:

	def __init__(self, port=10000):
		self.port = port
		

	def main(self):
		# Create a TCP/IP socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		# Bind the socket to the port
		server_address = ('localhost', self.port)
		print('starting up on %s port %s' % server_address)
		self.sock.bind(server_address)
		#self.sock.settimeout(1)#Para testes
		while True:
			print('\nwaiting for clients to connect')
			initialtime = time.time()
			curtime = time.time() - initialtime
			while curtime < 20:
				try:
					data, address = self.sock.recvfrom(1024)
				except (time.time() - curtime+initialtime) > 2: 
					curtime = time.time() - initialtime
				finally:
					curtime = 30
			
			if curtime < 30:
				self.sock.close()
			else:
				if data:
					print('received %s bytes from %s' % (len(data), address))
					print(data)		
			
					sent = self.sock.sendto(data, address)
					print('sent %s bytes back to %s' % (sent, address))

	def sendPhrase():
		print('\nfoo')

if __name__ == "__main__":
	sock=Server()
	sock.main()
