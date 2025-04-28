Ce programme fait la simulation d'un porte-avion permettant l'envoie d'avion, de faire de la maintenance sur ses catapultes et de faire atterrir ces avions.

Contient 2 fichiers:
- plane.py est une class permettant de créer un objet avion ayant sont état.
- carrier.py permet la gestion des commande envoyé par un utilisateur.
- deck.py est une class permetant de gérer le lancement et l'attérissage d'un avion.

## Prerequis
-Installer la librairie progressbar pour l'affichage avec la ligne de commande.
    pip install progressbar2
-VScode version 1.99.3
-Il faut que les trois fichiers soit dans le même dossier.

## Utilisation
Lancer à l'aide de VScode le fichier carrier.py
    L'utilisation de touche entrée par l'utilisatuer permet plusieurs actions.
    Lettre d'entree:    "v" affiche l'état des 4 catapultes
                        "r" lance un avion dans les airs
                        "s" affiche l'état des avions 
                        "1" ferme une des deux catapultes à l'avant du porte avion pour maintenance
                        "2" ouvre une catapultes à l'avant s'il y en avait une en maintenance
                        "3" ferme une des deux catapultes sur le coté du porte avion pour maintenance
                        "4" ouvre une catapultes à du coté s'il y en avait une en maintenance
                        "q" rappel tous les avions et ferme le programme
