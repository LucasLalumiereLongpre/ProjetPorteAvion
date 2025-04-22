"""
Author: Samuel Faucher
Date: 15 avril 2024
Description: Simulation des differentes phases d une avion sur un porte-avion
"""

import time
import random
from enum import Enum
import progressbar

# Etats possibles d un avion
class PlaneStates(Enum):
    InHangar = 1
    WaitingToLaunch = 2
    Launching = 3
    InAir = 4
    WaitingToLand = 5
    Landing = 6
    Retired = 7

# Objet regroupant les fonctionnalites d un avion
class Plane:
    def __init__(self, id):
        self.id = id
        self.status = PlaneStates.InHangar
        self.progress = 0
        self.catapult = "None"

    def getId(self):
        return self.id
    
    def getStatus(self):
        return self.status
    
    def setStatus(self, status):
        self.status = status

    def getCatapult(self):
        return self.catapult
    
    def setCatapult(self, catapult):
        self.catapult = catapult

    def launchPlane(self):
        import deck
        duration = 5  # seconds
        steps = 100
        interval = duration / steps  # time between increments

        while(self.getCatapult() == "None"):
            if (deck.tabCatapultesFront[0] == True or deck.tabCatapultesFront[1] == True):  #Si une catapulte en avant est dispo
                deck.semaphoreFront.acquire(blocking=False)  #Prend une cle
                self.setCatapult("Front")   #Indique que l'avion est sur une catapulte a l'avant
                if (deck.tabCatapultesFront[0] == True): #Si la catapulte est libre
                    deck.tabCatapultesFront[0] = False   #indique que la catpulte n'est plus disponible
                elif (deck.tabCatapultesFront[1] == True):
                    deck.tabCatapultesFront[1] = False
            elif (deck.tabCatapultesSide[0] == True or deck.tabCatapultesSide[1] == True): #Si une catapulte sur le cote est dispo
                deck.semaphoreSide.acquire(blocking=False)
                self.setCatapult("Side")    #Indique que l'avion est sur une catapulte sur le cote
                if (deck.tabCatapultesSide[0] == True): #Si la catapulte est libre
                    deck.tabCatapultesSide[0] = False   #indique que la catpulte n'est plus disponible
                elif (deck.tabCatapultesSide[1] == True):
                    deck.tabCatapultesSide[1] = False

        widgets = [' [',
         progressbar.Timer(format= 'elapsed time: %(elapsed)s'),
         '] ',
           progressbar.Bar('#' ),' (', 
           progressbar.ETA(), ') ',
          ]
        bar = progressbar.ProgressBar(max_value=steps, widgets=widgets).start()
        
        self.setStatus(PlaneStates.Launching)
        for i in range(steps + 1):  # 0 to 100 inclusive
            self.progress = i
            time.sleep(interval)
            bar.update(i)
        self.setStatus(PlaneStates.InAir)

    def getProgress(self):
        return self.progress

    def landPlane(self):
        duration = 5  # seconds
        steps = 100
        interval = duration / steps  # time between increments

        widgets = [' [',
         progressbar.Timer(format= 'elapsed time: %(elapsed)s'),
         '] ',
           progressbar.Bar('#' ),' (', 
           progressbar.ETA(), ') ',
          ]
        bar = progressbar.ProgressBar(max_value=steps, widgets=widgets).start()
        
        self.setStatus(PlaneStates.Landing)
        for i in range(steps + 1):  # 0 to 100 inclusive
            self.progress = i
            time.sleep(interval)
            bar.update(i)
        self.setStatus(PlaneStates.Retired)