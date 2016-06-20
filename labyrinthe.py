# -*-coding:Utf-8 -*
from fonctionlab import detail_choix
import random

"""Ce module contient la classe Labyrinthe."""

class Labyrinthe:

	"""Classe représentant un labyrinthe."""

	def __init__(self, robot, obstacles):
		"""initialisation de l'objet avec les listes robot et obstacles
		robot contiendra les positions des robots dans le labyrinthe et grille, le labyrinthe"""
		self.robot = robot
		self.grille = obstacles

	def deplacer_robot(self, choix, numero_joueur):
		""" Méthode permettant de déplacer le robot et de mettre à jour
		 sa nouvelle_position dans l'objet robot- elle prend en paramètre
		 le déplacement choisi par l'utilisateur """
		lettre,nb=detail_choix(choix)
		if choix[:-1] not in ('m','p'):
			if lettre=='s': #déplacement vers le bas
				nouvelle_position=[self.robot[numero_joueur][0]+nb,self.robot[numero_joueur][1]]
			elif lettre=='n':#déplacement vers le haut
				nouvelle_position=[self.robot[numero_joueur][0]-nb,self.robot[numero_joueur][1]]
			elif lettre=='o':#déplacement vers la gauche
				nouvelle_position=[self.robot[numero_joueur][0],self.robot[numero_joueur][1]-nb]
			elif lettre=='e':#déplacement vers la droite
				nouvelle_position=[self.robot[numero_joueur][0],self.robot[numero_joueur][1]+nb]

			if self.position_valide(nouvelle_position,lettre,nb): #si il n'y a pas de mur de la position initiale jusqu'à la nouvelle position
				self.robot[numero_joueur]=nouvelle_position #on met à jour l'attribut robot avec la nouvelle position
		else:
			print('m et p non traité')

	def position_valide(self,nouvelle_position,lettre,nb):
		""" Méthode permettant de savoir si la nouvelle position correspond à un mur"""
		i=0
		ligne=nouvelle_position[0]
		colonne=nouvelle_position[1]
		while i<nb:
			if lettre=='s':
				if self.grille.get((ligne-i,colonne))=='O': #si la nouvelle_position correspond à un mur
					return False
			if lettre=='n':
				if self.grille.get((ligne+i,colonne))=='O': #si la nouvelle_position correspond à un mur
					return False
			if lettre=='o':
				if self.grille.get((ligne,colonne+i))=='O': #si la nouvelle_position correspond à un mur
					return False
			if lettre=='e':
				if self.grille.get((ligne,colonne-i))=='O': #si la nouvelle_position correspond à un mur
					return False
			i+=1
		return True

	def verif_si_terminer(self):
		"""Méthode permettant de savoir si la partie est terminé"""
		for robot in self.robot: #on parcourt la liste des positions des robots
			if self.grille.get((robot[0],robot[1]))=='U': #si le robot est à la même position que le U
				ind = self.robot.index(robot)
				return True, ind #le client à gagner et terminer sera à True
			else:
				terminer = False #sinon on continuer
				ind=None
		return terminer, ind

	def labyrinthe_a_afficher(self):
		"""Cette méthode permet d'afficher la carte"""
		#on initialise les variables
		labyrinthe=''
		i=0
		ligne=1
		colonne=1
		while i<len(self.grille): #on boucle tant qu'on n'a pas affiché toute la grille
			if [ligne,colonne] in self.robot: #si on est à la position d'un robot, on le rajoute à labyrinthe
				labyrinthe=labyrinthe+'X'
			else:# sinon on rajoute le contenu de la grille à la position [ligne,colonne]
				labyrinthe=labyrinthe+self.grille[ligne,colonne]
				if self.grille[ligne,colonne]=='\n': #si c'est un saut de ligne, 
					colonne=0                                   #on reinitialise la colonne
					ligne+=1                                    # et la ligne
			i+=1
			colonne+=1
		return labyrinthe #on affiche le labyrinthe

	def donner_position_robot(self):
		"""Méthode permettant de renvoyer une position aleatoire pour le robot
		on parcourt la grille, on sélectionne les positions possibles du robot puis on en sélectionne une aléatoirement"""
		
		positions = []
		for position in self.grille: #on parcourt la grille du labyrinthe
			if self.grille[position] not in ('O','U','\n') and position not in self.robot: #s'il n'y a pas de mur, de U
																							#ni de robot à cette position
				positions.append(position) #on rajoute la position libre dans la liste positions
		position_aleatoire=random.choice(positions) #on choisie aléatoirement dans la liste une position
		return position_aleatoire # et on la retourne

	def envoyer_labyrinthe(self, clients_connectes):
		"""Méthode permettant d'envoyer le labyrinthe mis à jour à tous les clients connectés"""
		for connexion in clients_connectes: #pour chaque client
			numero_joueur=clients_connectes.index(connexion) #on recupère le numero du joueur
			ret_labyrinthe = self.labyrinthe_a_afficher() #on transforme le labyrinthe en chaine récupérée dans ret_labyrinthe
			coordonnees_robot_joueur=self.robot[numero_joueur] #on recupère la position du robot du joueur

			ligne=1
			colonne=1
			i=0
			#on personnalise le robot avant de l'envoyer avec un x minuscule pour le robot du client en cours de traitement
			#et X majuscule pour les robots des autres clients
			while i<len(ret_labyrinthe):
				if ret_labyrinthe[i]=='X':
					if (ligne!=coordonnees_robot_joueur[0] and colonne!=coordonnees_robot_joueur[1]):
						ret_labyrinthe=ret_labyrinthe[:i]+'x'+ret_labyrinthe[i+1:]
				elif ret_labyrinthe[i]=='\n':
					ligne+=1
				colonne+=1
				i+=1

			#on l'encode et on l'envoie au client
			ret_labyrinthe = ret_labyrinthe.encode()
			connexion.send(ret_labyrinthe)
