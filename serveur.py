# -*-coding:Utf-8 -*

"""Ce fichier contient le code du serveur du jeu.

Exécutez-le pour lancer le serveur

"""

import os
import socket
import select

from carte import Carte
from labyrinthe import Labyrinthe

from fonctionlab import *


print("Python serveur.py")

# On charge les cartes existantes
cartes = []
for nom_fichier in os.listdir("cartes"):
    if nom_fichier.endswith('.txt'):
        chemin = os.path.join("cartes",nom_fichier)
        nom_carte = nom_fichier[:-4].lower()
        with open(chemin, "r") as fichier:
            contenu = fichier.read()
        cartes.append(Carte(nom_carte,contenu)) # on rajoute à la liste la Carte qu'on a chargé

# On affiche les cartes existantes
print("Labyrinthes existants :")
for i, carte in enumerate(cartes):
    print("  {} - {}".format(i + 1, carte.nom))

# on attend le choix du joueur
choix = False
while not choix:
    try:
        reponse = input('Entrer votre choix: ')
        reponse = int(reponse)
        assert reponse in (1,2)
    except AssertionError:
        print('Vous devez choisir entre 1 ou 2')
        continue
    choix = True
carte_en_cours = cartes[reponse-1]

hote = ''
port = 12800

connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#on crée le socket
connexion_principale.bind((hote, port))#on connecte le socket
connexion_principale.listen(5)#on configure l'écoute du port

print("On attend les clients")

#initialisation des variables
labyrinthes = []
msg_recu = b''
numero_joueur = 0
clients_connectes = []
serveur_accept = True
terminer = False
while not terminer: # on fait tourner le serveur de jeux tant que la partie n'est pas terminée

    if serveur_accept:
        # On va vérifier que de nouveaux clients ne demandent pas à se connecter
        # Pour cela, on écoute la connexion_principale en lecture- On attend maximum 50ms
        connexions_demandees, wlist, xlist = select.select([connexion_principale],
        [], [], 0.05)
        for connexion in connexions_demandees:
            connexion_avec_client, infos_connexion = connexion.accept()
            # On ajoute le socket connecté à la liste des clients
            clients_connectes.append(connexion_avec_client)

            position_aleatoire_robot = carte_en_cours.labyrinthe.donner_position_robot() # on donne une position aléatoire au robot
                                                                    # en fonction des autres joueurs
            # on rajoute la position du robot du joueur(client)
            carte_en_cours.labyrinthe.robot.append([position_aleatoire_robot[0],position_aleatoire_robot[1]])

            print('{} joueur(s) connecté(s)'.format(numero_joueur+1))# le serveur affiche un message indiquant le nombre de joueurs

            #on envoie le labyrinthe à tous les connectés
            carte_en_cours.labyrinthe.envoyer_labyrinthe(clients_connectes)
            numero_joueur+=1

    # Maintenant, on écoute la liste des clients connectés
    # Les clients renvoyés par select sont ceux devant être lus (recv)
    # On attend là encore 50ms maximum
    # On enferme l'appel à select.select dans un bloc try
    # En effet, si la liste de clients connectés est vide, une exception
    # Peut être levée
    clients_a_lire = []
    try:
        clients_a_lire, wlist, xlist = select.select(clients_connectes,
        [], [], 0.05)
    except select.error:
        pass
    else:

        # On parcourt la liste des clients à lire
        for client in clients_a_lire:
            # Client est de type socket
            msg_recu = client.recv(1024) #je receptionne le paquet de 1024 octets
            # Peut planter si le message contient des caractères spéciaux
            msg_recu = msg_recu.decode() #je décode le paquet binaire
            msg_recu.lower()
            numero_joueur=clients_connectes.index(client)

            if msg_recu[-1:] == 'c':#La partie commence
                envoyer_message_clients(clients_connectes,"\nLa partie commence- Entrer votre deplacement n, s, o, e soit respectivement haut,bas, gauche, droite: \n")

            elif msg_recu[-1:] in ('n','s','o','e'):#on gère le deplacement du joueur
                carte_en_cours.labyrinthe.deplacer_robot(msg_recu,numero_joueur) #on deplace le robot

                carte_en_cours.labyrinthe.envoyer_labyrinthe(clients_connectes) #on envoie le labyrinthe aux clients

                terminer, indice = carte_en_cours.labyrinthe.verif_si_terminer() #on vérifie si le jeu est terminé

                if terminer: #si le jeu est terminé
                    for client in clients_connectes:
                        #on envoie un message au gagnant
                        if client==clients_connectes[indice]:
                            message_gagnant='\nBravo, vous avez gagné\n'
                            message_gagnantb=message_gagnant.encode()
                            client.send(message_gagnantb)
                        else: #et un autre message aux perdants
                            message_perdant='\nVous avez perdu\n'
                            message_perdantb=message_perdant.encode()
                            client.send(message_perdantb)

            elif msg_recu[-1:] == 'q':
                terminer=True


os.system("pause")
#Fin de la partie
print("Fermeture des connexions")
for client in clients_connectes:
    client.close()

connexion_principale.close()





