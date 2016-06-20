# -*-coding:Utf-8 -*
from fonctionlab import creer_labyrinthe_depuis_chaine
import os
import pickle

"""Ce module contient la classe Carte."""

class Carte:

    """Objet de transition entre un fichier et un labyrinthe.
    Les paramètres de la création de la Carte sont:
    - le nom String
    - la chaine String
    les attributs sont:
    - le nom du labyrinthe (ex: facile),
    - le labyrinthe qui sera un objet Labyrinthe créé à partir de la chaine """

    def __init__(self, nom, chaine):
        self.nom = nom
        self.labyrinthe = creer_labyrinthe_depuis_chaine(chaine)

    def __repr__(self):
        return "<Carte {}>".format(self.nom)

