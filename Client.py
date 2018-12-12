import socket
import threading
import sys

class Client:

	def __init__(self, port=10000):
		self.port = port
		

	def main(self):
		# Create a UDP socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		# Bind the socket to the port
		server_address = ('localhost', self.port)
		message = 'NEWCNX'.encode()
		condition = 'y'
		while condition == 'y' or condition == 't':

			# Send data
			if condition == 'y':
				message = 'NEWCNX'.encode()
			else:
				message = 'CNXACKACK'.encode()

			print('sending "%s"' % message.decode())
			sent = self.sock.sendto(message, server_address)

			# Receive response
			#print('waiting to receive')
			#data, server = self.sock.recvfrom(1024)
			#print('received "%s"' % data)

			condition = input("\ncontinue?(y/n)(t for ackack) ")
		
		print('closing socket')
		self.sock.close()


if __name__ == "__main__":
	sock=Client()
	sock.main()