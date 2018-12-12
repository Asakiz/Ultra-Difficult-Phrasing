import socket
import threading
import sys

class Server:

	def __init__(self, port=10000):
		self.port = port
		

	def main(self):
		# Create a TCP/IP socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		# Bind the socket to the port
		server_address = ('localhost', self.port)
		print(sys.stderr, 'starting up on %s port %s' % server_address)
		self.sock.bind(server_address)

		while True:
		    print(sys.stderr, '\nwaiting to receive message')
		    data, address = self.sock.recvfrom(1024)
		    
		    print(sys.stderr, 'received %s bytes from %s' % (len(data), address))
		    print(sys.stderr, data)
		    
		    if data:
		        sent = self.sock.sendto(data, address)
		        print(sys.stderr, 'sent %s bytes back to %s' % (sent, address))


if __name__ == "__main__":
	sock=Server()
	sock.main()
