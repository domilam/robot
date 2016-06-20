import unittest
import sys
sys.path.insert(0,'..')
from labyrinthe import *
from carte import *

class LabyrintheTest(unittest.TestCase):
	"""docstring for Labyrinthe_test pour tester la création d'un labyrinthe"""
	def test_labyrinthe(self):
		"""Test le fonctionnement de la création du labyrinthe."""
		robot = [[4,9],[5,10],[10,2]]
		grille={}
		grille[1,1]='O'
		grille[1,2]=' '
		lab1=Labyrinthe(robot,grille)
		elt=[5,10]
		# Vérifie que 'elt' est dans 'lab1.robot'
		self.assertIn(elt, lab1.robot)
		# Vérifie que 'lab1.grille[1,1]' contient bien 'O'
		self.assertEqual('O',lab1.grille[1,1])

class CarteTest(unittest.TestCase):
	"""docstring for CarteTest pour tester la création d'une carte"""
	def test_carte(self):
		"""Test le fonctionnement de la création de la carte"""
		nom="facile"
		chaine="O O OOO OO O"
		crt1=Carte(nom,chaine)
		self.assertEqual(' ',crt1.labyrinthe.grille[1,8])
		self.assertEqual(crt1.labyrinthe.robot,[])

class AfficheTest(unittest.TestCase):
	def test_affiche(self):
		"""Test le fonctionnement de l'affichage de la carte"""
		chaine="OOOOOOOOOO\nO O    O O\nO . OO   O\nO O O    O\nO OOOO O.O\nO O O    U\nO OOOOOO.O\nO O      O\nO O OOOOOO\nO . O    O\nOOOOOOOOOO"
		nom="facile"
		crt1=Carte(nom,chaine)
		chaine_labyrinthe=crt1.labyrinthe.labyrinthe_a_afficher()
		print(chaine_labyrinthe)

class DonnerPositionTest(unittest.TestCase):
	def test_donner_position_robot(self):
		"""test de la méthode donner_position_robot"""
		chaine = "OOOOOOOOOO\nO O    O O\nO . OO   O\nO O O    O\nO OOOO O.O\nO O O    U\nO OOOOOO.O\nO O      O\nO O OOOOOO\nO . O    O\nOOOOOOOOOO"
		nom = "facile"
		crt1 = Carte(nom,chaine)
		crt1.labyrinthe.robot=[[3,8],[2,5]]
		position_aleatoire = crt1.labyrinthe.donner_position_robot()
		self.assertNotIn(position_aleatoire, crt1.labyrinthe.robot)

unittest.main()
