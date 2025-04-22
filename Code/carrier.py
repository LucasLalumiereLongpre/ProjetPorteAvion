"""
Author: Marc-Antoine Sauve et Lucas Lalumiere-Longpre
Date: 11 avril 2025
Description: Simulation d un porte-avion commande par des touches de clavier
"""

import time
import threading
from threading import Thread, Semaphore, Condition
from multiprocessing import Process, Value, Queue
import multiprocessing
from ctypes import c_bool
import ctypes
import sys
import select
from plane import Plane, PlaneStates

g_carrier_active = multiprocessing.Value('b', True) 

"""Vérifie si une touche est pressée sans blocage."""
def is_key_pressed():
    return select.select([sys.stdin], [], [], 0)[0]

"""Lit la touche appuyée."""
def get_key_pressed():
    return sys.stdin.read(1)


def getCatapultStatus(tabCatapultesAvant, tabCatapultesAvantMaintenance, tabCatapultesCote, tabCatapultesCoteMaintenance):
    print("\n--- État des catapultes ---")
    for i in range(2):
        # Catapultes avant
        if tabCatapultesAvantMaintenance[i]:
            etat = "EN MAINTENANCE"
        elif tabCatapultesAvant[i]:
            etat = "DISPONIBLE"
        else:
            etat = "OCCUPÉE"
        print(f"Catapulte avant {i+1} : {etat}")
        
    for i in range(2):
        # Catapultes côté
        if tabCatapultesCoteMaintenance[i]:
            etat = "EN MAINTENANCE"
        elif tabCatapultesCote[i]:
            etat = "DISPONIBLE"
        else:
            etat = "OCCUPÉE"
        print(f"Catapulte côté {i+1} : {etat}")
    print("---------------------------\n")




# Fonction qui lit le clavier periodiquement (a partir dans un thread a part)
# Inputs: un booleen qui permet de sortir du thread de facon propre, la queue de message recu
# Output: NA
def dashboard(carrier_active, inputQueue,
              tabCatapultesAvant, tabCatapultesAvantMaintenance, sem_catapultesAvant,
              tabCatapultesCote, tabCatapultesCoteMaintenance, sem_catapultesCote):
    print("Dashboard online")
    while carrier_active.value:
        if is_key_pressed():
            input_str = get_key_pressed()
            if input_str in ("r", "l"):
                inputQueue.put(input_str)
            elif input_str == "q":
                ##carrier_active.value = False
                inputQueue.put(input_str)
            elif input_str == "1":
                if tabCatapultesAvant[0] == True:
                    sem_catapultesAvant.acquire()
                    tabCatapultesAvant[0]=False
                    tabCatapultesAvantMaintenance[0]=True
                    print("*** One front catapult locked for maintenance ***")
                elif tabCatapultesAvant[1]  == True:
                    sem_catapultesAvant.acquire()
                    tabCatapultesAvant[1]=False
                    tabCatapultesAvantMaintenance[1]=True
                    print("*** One front catapult locked for maintenance ***")
                elif tabCatapultesAvantMaintenance[1]==True and tabCatapultesAvantMaintenance[0]==True:
                    print("*** All catapults in front are already in maintenance ***")
                else :
                    print("*** front catapult(s) in use, try again ***")
            elif input_str == "2":
                if tabCatapultesAvantMaintenance[0] == True:
                    tabCatapultesAvant[0]=True
                    tabCatapultesAvantMaintenance[0] = False
                    sem_catapultesAvant.release()
                    print("*** One front catapult unlocked***")

                elif tabCatapultesAvantMaintenance[1] == True:
                    tabCatapultesAvant[1]=True
                    tabCatapultesAvantMaintenance[1] = False
                    sem_catapultesAvant.release()
                    print("*** One front catapult unlocked***")
                else :
                    print("*** No front catapult in maintenance ***")
            elif input_str == "3":
                if tabCatapultesCote[0] == True:
                    sem_catapultesCote.acquire()
                    tabCatapultesCote[0]=False
                    tabCatapultesCoteMaintenance[0]=True
                    print("*** One side catapult locked for maintenance ***")
                elif tabCatapultesCote[1]  == True:
                    sem_catapultesCote.acquire()
                    tabCatapultesCote[1]=False
                    tabCatapultesCoteMaintenance[1]=True
                    print("*** One side catapult locked for maintenance ***")
                elif tabCatapultesCoteMaintenance[1]==True and tabCatapultesCoteMaintenance[0]==True:
                    print("*** All catapults on the side are already in maintenance ***")
                else :
                    print("*** side catapult(s) in use, try again ***")
            elif input_str == "4":
                if tabCatapultesCoteMaintenance[0] == True:
                    tabCatapultesCote[0]=True
                    tabCatapultesCoteMaintenance[0] = False
                    sem_catapultesCote.release()
                    print("*** One side catapult unlocked***")

                elif tabCatapultesCoteMaintenance[1] == True:
                    tabCatapultesCote[1]=True
                    tabCatapultesCoteMaintenance[1] = False
                    sem_catapultesCote.release()
                    print("*** One side catapult unlocked***")
                else :
                    print("*** No side catapultin maintenance ***")
            elif input_str == "s":
                getCatapultStatus(tabCatapultesAvant, tabCatapultesAvantMaintenance, tabCatapultesCote, tabCatapultesCoteMaintenance)

    print("Dashboard offline")
    keyPress_thread.join()


if __name__ == "__main__":
     # Flag pour arrêter proprement le thread
    carrier_active = Value(ctypes.c_bool, True)

    # File de messages
    inputQueue = Queue()

    sem_catapultesAvant = threading.Semaphore(2)
    sem_catapultesCote = threading.Semaphore(2)

    condAvant = Condition()
    condCote = Condition()

    tabCatapultesAvant = [True, True]
    tabCatapultesCote = [True, True]
    tabCatapultesAvantMaintenance = [False, False]
    tabCatapultesCoteMaintenance = [False, False]

    keyPress_thread = threading.Thread(
    target=dashboard,
    args=(
        g_carrier_active,
        inputQueue,
        tabCatapultesAvant,
        tabCatapultesAvantMaintenance,
        sem_catapultesAvant,
        tabCatapultesCote,
        tabCatapultesCoteMaintenance,
        sem_catapultesCote
    )
)
    keyPress_thread.start()
    
    while(1) :
        {



        }
 
    # Exemple de boucle principale simulée
    try:
        while True:
            if not inputQueue.empty():
                message = inputQueue.get()
                print(f"Reçu : {message}")
                if message == "exit":
                    carrier_active.value = False
                    break
    except KeyboardInterrupt:
        carrier_active.value = False

    print("Programme terminé.")
