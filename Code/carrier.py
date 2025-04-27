"""
Author: Marc-Antoine Sauve et Lucas Lalumiere-Longpre
Date: 11 avril 2025

A faire : 


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
import os
from deck import Deck

g_carrier_active = multiprocessing.Value('b', True) 

"""Vérifie si une touche est pressée sans blocage."""
def is_key_pressed():
    return select.select([sys.stdin], [], [], 0)[0]

"""Lit la touche appuyée."""
def get_key_pressed():
    return sys.stdin.read(1)

def getCatapultStatus(tabCatapultesFront, tabCatapultesFrontMaintenance, tabCatapultesSide, tabCatapultesSideMaintenance):
    print("\n--- État des catapultes ---")
    for i in range(2):
        # Catapultes avant
        if tabCatapultesFrontMaintenance[i]:
            etat = "EN MAINTENANCE"
        elif tabCatapultesFront[i]:
            etat = "DISPONIBLE"
        else:
            etat = "OCCUPÉE"
        print(f"Catapulte avant {i+1} : {etat}")
        
    for i in range(2):
        # Catapultes côté
        if tabCatapultesSideMaintenance[i]:
            etat = "EN MAINTENANCE"
        elif tabCatapultesSide[i]:
            etat = "DISPONIBLE"
        else:
            etat = "OCCUPÉE"
        print(f"Catapulte côté {i+1} : {etat}")
    print("---------------------------\n")

# Fonction qui lit le clavier periodiquement (a partir dans un thread a part)
# Inputs: un booleen qui permet de sortir du thread de facon propre, la queue de message recu
# Output: NA
def dashboard(carrier_active, inputQueue,
              tabCatapultesFront, tabCatapultesFrontMaintenance, semaphoreFront,
              tabCatapultesSide, tabCatapultesSideMaintenance, semaphoreSide):
    print("Dashboard online")
    while carrier_active.value:
        if is_key_pressed():
            input_str = get_key_pressed()
            if input_str in ("r", "l", "s"):
                inputQueue.put(input_str)
            elif input_str == "q":
                inputQueue.put(input_str)
                deck_process.join()
                carrier_active.value = False

            elif input_str == "1":
                if tabCatapultesFront[0] == True:
                    semaphoreFront.acquire()
                    tabCatapultesFront[0]=False
                    tabCatapultesFrontMaintenance[0]=True
                    print("*** One front catapult locked for maintenance ***")
                elif tabCatapultesFront[1]  == True:
                    semaphoreFront.acquire()
                    tabCatapultesFront[1]=False
                    tabCatapultesFrontMaintenance[1]=True
                    print("*** One front catapult locked for maintenance ***")
                elif tabCatapultesFrontMaintenance[1]==True and tabCatapultesFrontMaintenance[0]==True:
                    print("*** All catapults in front are already in maintenance ***")
                else :
                    print("*** front catapult(s) in use, try again ***")
            elif input_str == "2":
                if tabCatapultesFrontMaintenance[0] == True:
                    tabCatapultesFront[0]=True
                    tabCatapultesFrontMaintenance[0] = False
                    semaphoreFront.release()
                    print("*** One front catapult unlocked***")

                elif tabCatapultesFrontMaintenance[1] == True:
                    tabCatapultesFront[1]=True
                    tabCatapultesFrontMaintenance[1] = False
                    semaphoreFront.release()
                    print("*** One front catapult unlocked***")
                else :
                    print("*** No front catapult in maintenance ***")
            elif input_str == "3":
                if tabCatapultesSide[0] == True:
                    semaphoreSide.acquire()
                    tabCatapultesSide[0]=False
                    tabCatapultesSideMaintenance[0]=True
                    print("*** One side catapult locked for maintenance ***")
                elif tabCatapultesSide[1]  == True:
                    semaphoreSide.acquire()
                    tabCatapultesSide[1]=False
                    tabCatapultesSideMaintenance[1]=True
                    print("*** One side catapult locked for maintenance ***")
                elif tabCatapultesSideMaintenance[1]==True and tabCatapultesSideMaintenance[0]==True:
                    print("*** All catapults on the side are already in maintenance ***")
                else :
                    print("*** side catapult(s) in use, try again ***")
            elif input_str == "4":
                if tabCatapultesSideMaintenance[0] == True:
                    tabCatapultesSide[0]=True
                    tabCatapultesSideMaintenance[0] = False
                    semaphoreSide.release()
                    print("*** One side catapult unlocked***")

                elif tabCatapultesSideMaintenance[1] == True:
                    tabCatapultesSide[1]=True
                    tabCatapultesSideMaintenance[1] = False
                    semaphoreSide.release()
                    print("*** One side catapult unlocked***")
                else :
                    print("*** No side catapultin maintenance ***")
            elif input_str == "v":
                getCatapultStatus(tabCatapultesFront, tabCatapultesFrontMaintenance, tabCatapultesSide, tabCatapultesSideMaintenance)
    tabCatapultesFront = [True, True]
    tabCatapultesSide = [True, True]
    print("Dashboard offline")
    #keyPress_thread.join()

if __name__ == "__main__":
    manager = multiprocessing.Manager()
     # Flag pour arrêter proprement le thread
    carrier_active = Value(ctypes.c_bool, True)

    # File de messages
    inputQueue = Queue()

    semaphoreFront = multiprocessing.Semaphore(2)
    semaphoreSide = multiprocessing.Semaphore(2)

    condAvant = Condition()
    condCote = Condition()

    tabCatapultesFront = manager.list([True, True])
    tabCatapultesSide = manager.list([True, True])


    tabCatapultesFrontMaintenance = [False, False]
    tabCatapultesSideMaintenance = [False, False]
    # Créer un processus pour exécuter deck.py
    deck = Deck(tabCatapultesFront, tabCatapultesSide, semaphoreFront, semaphoreSide, inputQueue)
    deck_process = multiprocessing.Process(target=deck.runDeck)
    deck_process.start()

    keyPress_thread = threading.Thread(
    target=dashboard,
    args=(
        g_carrier_active,
        inputQueue,
        tabCatapultesFront,
        tabCatapultesFrontMaintenance,
        semaphoreFront,
        tabCatapultesSide,
        tabCatapultesSideMaintenance,
        semaphoreSide
    )
    )
    keyPress_thread.start()
    while(carrier_active.value):
        if(KeyboardInterrupt):
            carrier_active.value = False
            deck_process.join()
            keyPress_thread.join()

    keyPress_thread.join()