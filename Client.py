import socket
import threading
import sys

class Client:

	def __init__(self, port=10000):
		self.port = port
		

	def main(self):
		# Create a UDP socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		server_address = ('localhost', self.port)
		message = 'This is the message.  It will be repeated.'.encode()

		try:

		    # Send data
		    print(sys.stderr, 'sending "%s"' % message)
		    sent = self.sock.sendto(message, server_address)

		    # Receive response
		    print(sys.stderr, 'waiting to receive')
		    data, server = self.sock.recvfrom(1024)
		    print(sys.stderr, 'received "%s"' % data)

		finally:
		    print(sys.stderr, 'closing socket')
		    self.sock.close()


if __name__ == "__main__":
	sock=Client()
	sock.main()