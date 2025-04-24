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

    def launchPlane(self, tabCatapultesFront, tabCatapultesSide, semaphoreFront, semaphoreSide):
        duration = 5  # seconds
        steps = 100
        interval = duration / steps  # time between increments

        while(self.getCatapult() == "None"):
            if (tabCatapultesFront[0] == True or tabCatapultesFront[1] == True):  #Si une catapulte en avant est dispo
                semaphoreFront.acquire(blocking=False)  #Prend une cle
                self.setCatapult("Front")   #Indique que l'avion est sur une catapulte a l'avant
                if (tabCatapultesFront[0] == True): #Si la catapulte est libre
                    tabCatapultesFront[0] = False   #indique que la catpulte n'est plus disponible
                elif (tabCatapultesFront[1] == True):
                    tabCatapultesFront[1] = False
            elif (tabCatapultesSide[0] == True or tabCatapultesSide[1] == True): #Si une catapulte sur le cote est dispo
                semaphoreSide.acquire(blocking=False)
                self.setCatapult("Side")    #Indique que l'avion est sur une catapulte sur le cote
                if (tabCatapultesSide[0] == True): #Si la catapulte est libre
                    tabCatapultesSide[0] = False   #indique que la catpulte n'est plus disponible
                elif (tabCatapultesSide[1] == True):
                    tabCatapultesSide[1] = False

        widgets = [' [',
         progressbar.Timer(format= 'Plane launching: %(elapsed)s'),
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
        print('\n')
        self.setStatus(PlaneStates.InAir)
        if(self.getCatapult() == "Front"):
            semaphoreFront.release()
            if (tabCatapultesFront[0] == False): 
                    tabCatapultesFront[0] = True  
            elif (tabCatapultesFront[1] == False):
                    tabCatapultesFront[1] = True
        elif(self.getCatapult() == "Side"):
            semaphoreSide.release()
            if (tabCatapultesSide[0] == False): 
                    tabCatapultesSide[0] = True  
            elif (tabCatapultesSide[1] == False):
                    tabCatapultesSide[1] = True

    def getProgress(self):
        return self.progress

    def landPlane(self, tabCatapultesSide, semaphoreSide):
        #Prend les deux cles du semaphore
        semaphoreSide.acquire(blocking=False)
        semaphoreSide.acquire(blocking=False)
        tabCatapultesSide[0] = False
        tabCatapultesSide[1] = False

        duration = 5  # seconds
        steps = 100
        interval = duration / steps  # time between increments

        widgets = [' [',
         progressbar.Timer(format= 'Plane landing: %(elapsed)s'),
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
        print('\n')
        self.setStatus(PlaneStates.Retired)
        semaphoreSide.release()
        semaphoreSide.release()
        tabCatapultesSide[0] = True
        tabCatapultesSide[1] = True