import socket
import threading
import sys
import time
import random

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
		return

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
		t1 = threading.Thread(target=self.listener, args=('NEWCNX',))
		t1.start()
		t1.join()
		self.player1 = self.address
		self.threadfinished = False
		t1 = threading.Thread(target=self.sender, args=('CNXACK', self.player1))
		t2 = threading.Thread(target=self.listener, args=('CNXACKACK',))
		t1.start()
		t2.start()
		t1.join()
		t2.join()
		
		#copypaste for player2, so cuidar pra nao deixar o mesmo player conectar 2x
		self.threadfinished = False
		t1 = threading.Thread(target=self.listener, args=('NEWCNX',))
		t1.start()
		t1.join()
		self.player2 = self.address
		self.threadfinished = False
		t1 = threading.Thread(target=self.sender, args=('CNXACK', self.player2))
		t2 = threading.Thread(target=self.listener, args=('CNXACKACK',))
		t1.start()
		t2.start()
		t1.join()
		t2.join()

	def switchzao(self, argument):
	    switcher = {
	        1: "Frase Simples",
	        2: "As coisas começam a complicar",
	        3: "ÀlgÚnS ÃcêNTöS",
	        4: "@#$%*@$&&¨@$%*#",
	        5: "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...",
	        6: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec interdum nulla ipsum, vitae rhoncus sem ultricies eu. Praesent vel ligula libero. Nunc eu placerat purus, ut vestibulum felis. Morbi placerat pellentesque sem a facilisis. Duis blandit enim nunc, vel cursus lectus egestas ac. Fusce nec enim feugiat, porttitor erat non, malesuada sapien. Vestibulum ullamcorper est quis ullamcorper blandit. Suspendisse potenti. Proin dignissim augue et dictum vulputate. Sed luctus vitae lectus eu molestie. Etiam suscipit, ex ut euismod scelerisque, eros risus sagittis dui, sed eleifend ex orci id orci. Nulla congue pulvinar nisi, ut ornare leo aliquet vitae. Vestibulum tristique sed turpis sed tincidunt.",
	    }
	    return switcher.get(argument, "fail")

	def prepareGame(self):
		escolha = random.randint(1, 6)
		return self.switchzao(escolha)

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
		playeripaddress, playerport = self.player2
		print('\nplayer 2 connected, IP: %s' % playeripaddress)
		self.frase = self.prepareGame()
		print('\n%s' % self.frase)
		

if __name__ == "__main__":
	sock=Server()
	sock.main()
