from threading import Thread
import socket
import sys
"""Deux class permettant de gérer en parallèle, du coté client, la réception et l'envoi"""

class Reception(Thread):
	"""Class de réception héritant de Thread"""
	def __init__(self,connexion_avec_serveur):
		Thread.__init__(self)
		self.connexion=connexion_avec_serveur

	def run(self):
		"""Code à exécuter pendant l'exécution du thread."""
		while (True):
			msg_recu = self.connexion.recv(1024) #je recois
			msg_recu = msg_recu.decode() #je decode
			print(msg_recu)

class Envoi(Thread):
	"""Class d'envoi héritant de Thread"""
	def __init__(self,connexion_avec_serveur):
		Thread.__init__(self)
		self.connexion = connexion_avec_serveur
		self.envoye=''

	def run(self):
		"""Code à exécuter pendant l'exécution du thread."""
		while (True):
			self.envoye = input("\nSaisissez la commande >> \n").lower()
			self.envoye = self.envoye.encode() #je code le message en binaire
			self.connexion.send(self.envoye) #j'envoi le message
			if self.envoye==b'q':
				sys.exit()