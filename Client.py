import socket
import threading
import sys
import time

#	cd Documents\Faculdade\Redes\Ultra-Difficult-Phrasing

class Client:

	def __init__(self, port=10000):
		self.port = port
		self.player = '0'
		self.frase = ''
		self.fraseatual = ''
#taken from https://stackoverflow.com/questions/510357/python-read-a-single-character-from-the-user
	def getChar(self):
		try:
			# for Windows-based systems
			import msvcrt # If successful, we are on Windows
			return msvcrt.getch()

		except ImportError:
			# for POSIX-based systems (with termios & tty support)
			import tty, sys, termios  # raises ImportError if unsupported

			fd = sys.stdin.fileno()
			oldSettings = termios.tcgetattr(fd)

			try:
				tty.setcbreak(fd)
				answer = sys.stdin.read(1)
			finally:
				termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)

			return answer

	def sender(self, message, address):
		self.threadfinished = False
		while(self.threadfinished == False):
			self.sock.sendto(message.encode(), address)
			#print('\nsending %s again..' % message)
			time.sleep(1)
		return

	def listener(self, message):
		data, address = self.sock.recvfrom(1024)
		while data.decode() != message:
			data, address = self.sock.recvfrom(1024)
		self.threadfinished = True
		self.data = data
		self.address = address
		return

	def definePlayerListener(self, message):
		data, address = self.sock.recvfrom(1024)
		while data.decode() != message+'1' and data.decode() != message+'2':
			data, address = self.sock.recvfrom(1024)
		if data.decode() == message+'1':
			self.player = '1'
		else:
			self.player = '2'
		print(self.player+'\n')
		self.threadfinished = True
		self.data = data
		self.address = address
		return

	def phraseListener(self, message):
		data, address = self.sock.recvfrom(1024)
		while data.decode()[0:5] != message[0:5]:
			data, address = self.sock.recvfrom(1024)
		self.frase = data.decode()[6:len(data.decode())]
		self.threadfinished = True
		self.data = data
		self.address = address
		return

	def tenTimesSender(self, message, address):
		for vezes in range(0,10):
			print('jogo comeca em %d segundos' % (10-vezes))
			self.sock.sendto(message.encode(), address)
			time.sleep(1)
		return

	def newCnx(self):
		#self.threadfinished = False
		#t1 = threading.Thread(target=self.sender, args=('NEWCNX', self.server_address))
		t2 = threading.Thread(target=self.definePlayerListener, args=('CNXACK',))
		#t1.start()
		#t2.start()
		#t1.join()
		#t2.join()

		self.sock.sendto('NEWCNX'.encode(), self.server_address) #sender na thread tava dando ruim, nao sei pq
		time.sleep(1)
		t2.start()
		t2.join()

		print('\nrecebendo frase para iniciar o jogo')
		self.threadfinished = False
		t1 = threading.Thread(target=self.sender, args=('CNXACKACK', self.server_address))
		t2 = threading.Thread(target=self.phraseListener, args=('PHRASE',))
		t1.start()
		t2.start()
		t1.join()
		t2.join()
		self.tenTimesSender('PHRACK'+self.player, self.server_address)
		return
		
	def letterSender(self):
		while self.threadfinished == False:
			letter = self.getChar()
			print(letter)
			if(letter == b'\x08'):
				msgletter = 'BACKSP'+self.player+'CE'
			else:
				msgletter = 'LETTER'+self.player+letter.decode()
			self.sock.sendto(msgletter.encode(), self.server_address)
		return

	def pprinter(self):
		print('\n\n'+self.frase+'\n\n'+self.fraseatual+'\n\n')

	def phraseUpdater(self):
		while self.threadfinished == False:
			self.pprinter()
			data, address = self.sock.recvfrom(1024)
			while data.decode()[0:7] != 'PHRUPDT'+self.player and data.decode() != 'WINNER' and data.decode() != 'LOSER':
				data, address = self.sock.recvfrom(1024)
				print(data.decode())
			if(data.decode() == 'WINNER'):
				self.threadfinished = True
				self.gameover = 'winner'
			elif(data.decode() == 'LOSER'):
				self.threadfinished = True
				self.gameover = 'loser'
			else:
				self.fraseatual = data.decode()[8:len(data.decode())]
			#pprinter()
		return
	

	def playing(self):
		self.threadfinished = False
		t1 = threading.Thread(target=self.letterSender)
		t2 = threading.Thread(target=self.phraseUpdater)
		t1.start()
		t2.start()
		t1.join()
		t2.join()
		return













	def main(self):
		# Create a UDP socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		# Bind the socket to the port
		self.server_address = ('localhost', self.port)
		
		self.newCnx()

		self.playing()

		#process gameover


		print('\nclosing socket')
		self.sock.close()


if __name__ == "__main__":
	sock=Client()
	sock.main()