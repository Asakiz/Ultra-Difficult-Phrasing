import socket
import threading
import sys
import time
import random

class Server:

	def __init__(self, port=10000):
		self.port = port
		self.winner = '0'
		

	def sender(self, message, address):
		self.threadfinished = False
		while(self.threadfinished == False):
			self.sock.sendto(message.encode(), address)
			print('\nsending again..')
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

	def sender2(self, message, address):
		self.threadfinished2 = False
		while(self.threadfinished2 == False):
			self.sock.sendto(message.encode(), address)
			print('\nsending again..')
			time.sleep(1)
		return

	def listener2(self, message):
		data, address = self.sock.recvfrom(1024)
		while data.decode() != message:
			data, address = self.sock.recvfrom(1024)
		self.threadfinished2 = True
		self.data2 = data
		self.address2 = address
		return

	def waitNewCnx(self):
		self.threadfinished = False
		t1 = threading.Thread(target=self.listener, args=('NEWCNX',))
		t1.start()
		t1.join()
		self.player1 = self.address
		self.threadfinished = False
		t1 = threading.Thread(target=self.sender, args=('CNXACK1', self.player1))
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
		t1 = threading.Thread(target=self.sender, args=('CNXACK2', self.player2))
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
	        6: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec interdum nulla ipsum, vitae rhoncus sem ultricies eu. Praesent vel ligula libero. Nunc eu placerat purus, ut vestibulum felis. Morbi placerat pellentesque sem a facilisis. Duis blandit enim nunc, vel cursus lectus egestas ac. Fusce nec enim feugiat, porttitor erat non, malesuada sapien. Vestibulum ullamcorper est quis ullamcorper blandit. Suspendisse potenti.",
	    }
	    return switcher.get(argument, "fail")

	def prepareGame(self):
		escolha = random.randint(1, 6)
		return self.switchzao(escolha)

	def letterListener(self):
		while True:
			time.sleep(0.2) #tentativa de adicionar um delay para complicar os participantes já que o dummynet nao funcionou
			data, address = self.sock.recvfrom(1024)
			if data.decode()[6] == '1':
				if data.decode()[0] == 'L':#LETTER1%, % = caractere
					self.frasep1 += data.decode()[7]
				else:#caso de resposta BACKSP1CE
					self.frasep1 = self.frasep1[0:-1]
			else:
				if data.decode()[0] == 'L':#LETTER2%, % = caractere
					self.frasep2 += data.decode()[7]
				else:#caso de resposta BACKSP2CE
					self.frasep2 = self.frasep2[0:-1]
			if(self.frase == self.frasep1):
				self.winner = '1'
				break
			else if(self.frase == self.frasep2):
				self.winner = '2'
				break

	def phraseUpdater(self):
		while self.winner == '0':
			msg1 = 'PHRUPDT1'+self.frasep1
			self.sock.sendto(msg1.encode(), player1)
			msg2 = 'PHRUPDT2'+self.frasep2
			self.sock.sendto(msg1.encode(), player2)
			time.sleep(1)

	def letterRecog(self):
		self.frasep1 = ""
		self.frasep2 = ""
		t1 = threading.Thread(target=self.phraseUpdater)
		t2 = threading.Thread(target=self.letterListener)
		t1.start()
		t2.start()
		t1.join()
		t2.join()
		
	def finishingGame(self):
		self.threadfinished = False
		self.threadfinished2 = False
		if self.winner == '1':
			p1result = 'WINNER'
			p2result = 'LOSER'
		else:
			p2result = 'WINNER'
			p1result = 'LOSER'

		t1 = threading.Thread(target=self.sender, args=(p1result, self.player1))
		t2 = threading.Thread(target=self.listener, args=('ACK_ENDGAME1',))
		t3 = threading.Thread(target=self.sender2, args=(p2result, self.player2))
		t4 = threading.Thread(target=self.listener2, args=('ACK_ENDGAME2',))
		t1.start()
		t2.start()
		t3.start()
		t4.start()
		t1.join()
		t2.join()
		t3.join()
		t4.join()


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
		t1 = threading.Thread(target=self.sender, args=('PHRASE'+self.frase, self.player1))
		t2 = threading.Thread(target=self.listener, args=('PHRACK1',))
		t3 = threading.Thread(target=self.sender2, args=('PHRASE'+self.frase, self.player2))
		t4 = threading.Thread(target=self.listener2, args=('PHRACK2',))
		t1.start()
		t2.start()
		t3.start()
		t4.start()
		t1.join()
		t2.join()
		t3.join()
		t4.join()

		self.letterRecog()#funcao que roda o jogo

		self.finishingGame()#envia resultados e fecha o servidor


		

if __name__ == "__main__":
	sock=Server()
	sock.main()
