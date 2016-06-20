import socket
from thread_client import *

connexion_avec_serveur=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #je créé le socket
connexion_avec_serveur.connect(('localhost',12800)) #je connecte le socket
print('connecté')

#création des threads
envoye=Envoi(connexion_avec_serveur)
recu=Reception(connexion_avec_serveur)

#lancement des threads
recu.start()
envoye.start()

#Attend que les threads se terminent
recu.join()
envoye.join()

#ferme la connexion client
connexion_avec_serveur.close()
