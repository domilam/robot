def creer_labyrinthe_depuis_chaine(chaine):
    """ fonction permettant de créer un objet Labyrinthe
    à partir de la chaine reçu en paramètre"""
    from labyrinthe import Labyrinthe

    i=0 #l'indice du caractère dans la chaine
    obstacles={} # contiendra la position des obstacles en fonction de la colonne et de la ligne
    ligne=1
    colonne=1
    while i < len(chaine): #on boucle tant  qu'on n'est pas à la fin de la chaine
        # on enregistrer la position de l'obstacles
        obstacles[ligne,colonne]=chaine[i]
        if chaine[i]=='\n': # on verifie si on est à la fin d'une ligne
            ligne+=1 # on incrémente la ligne lorsqu'on passe à la ligne et on met la colonne à 0 puisqu'elle sera incrémentée
            colonne=0 
        i+=1
        colonne+=1 #on incrémente la colonne
    return Labyrinthe([],obstacles) #on retourne l'objet qu'on créé, avec la position du robot et des obstacles

def detail_choix(choix):
    """Méthode permettant de séparer la lettre et nombre nb dans le choix du déplacement"""
    lettre=choix[-1:] # la lettre (la direction) c'est le dernier caractère du choix
    if len(choix)>1 and choix[:-1] not in ('m','p'):
        nb=int(choix[:-1])#le nombre c'est le choix sans le dernier caractere puis converti en entier
    else:
        nb=1 # si il n'y a qu'une lettre, on lui donne la valeur 1
    return lettre,nb

def envoyer_message_clients(clients_connectes,message_a_envoyer):
    """Méthode permettant d'envoyer un message à tous les clients"""
    for connexion in clients_connectes:
        message_binaire = message_a_envoyer.encode()
        connexion.send(message_binaire)
