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
    def __init__(self, id,tabCatapultesFront, tabCatapultesSide, semaphoreFront, semaphoreSide,):
        self.id = id
        self.status = PlaneStates.InHangar  #Etat de l'avion
        self.progress = 0   #Valeur de la barre de progres actuelle
        self.catapult = "None"  #Catapulte choisie
        self.tabCatapultesFront = tabCatapultesFront
        self.tabCatapultesSide = tabCatapultesSide
        self.semaphoreFront = semaphoreFront
        self.semaphoreSide = semaphoreSide

    #Fonction qui retourne l'id de l'avion
    def getId(self):
        return self.id
    
    #Retourne le status de l'avion
    def getStatus(self):
        return self.status
    
    #Retourne le nom de l'etat de l'avion
    def getStatusName(self):
         return self.status.name
    
    #Fonction pour assigner un nouvel etat
    def setStatus(self, status):
        self.status = status

    #Fonction qui retourne la catapulte, soit None, Side ou Front
    def getCatapult(self):
        return self.catapult
    
    #Fonction qui assigne la catapulte
    def setCatapult(self, catapult):
        self.catapult = catapult

    #methode pour lancer un avion
    def launchPlane(self):
        duration = 20  #En secondes
        steps = 100    #De 0 a 100
        interval = duration / steps  #temps entre increment

        while(self.getCatapult() == "None"):    #tant que l'avion n'a pas choisi de catapulte
            if (self.tabCatapultesFront[0] == True or self.tabCatapultesFront[1] == True):  #Si une catapulte en avant est dispo
                self.semaphoreFront.acquire()  #Prend une cle
                self.setCatapult("Front")   #Indique que l'avion est sur une catapulte a l'avant
                if (self.tabCatapultesFront[0] == True): #Si la catapulte est libre
                    self.tabCatapultesFront[0] = False   #indique que la catpulte n'est plus disponible
                elif (self.tabCatapultesFront[1] == True):
                    self.tabCatapultesFront[1] = False
            elif (self.tabCatapultesSide[0] == True or self.tabCatapultesSide[1] == True): #Si une catapulte sur le cote est dispo
                self.semaphoreSide.acquire()
                self.setCatapult("Side")    #Indique que l'avion est sur une catapulte sur le cote
                if (self.tabCatapultesSide[0] == True): #Si la catapulte est libre
                    self.tabCatapultesSide[0] = False   #indique que la catpulte n'est plus disponible
                elif (self.tabCatapultesSide[1] == True):
                    self.tabCatapultesSide[1] = False

        widgets = [' [',
         progressbar.Timer(format= 'Plane launching: %(elapsed)s'), #Barre de progres
         '] ',
           progressbar.Bar('#' ),' (', 
           progressbar.ETA(), ') ',
          ]
        bar = progressbar.ProgressBar(max_value=steps, widgets=widgets).start() #Demarre la barre de progres
        
        self.setStatus(PlaneStates.Launching)   #Indique que l'avion decolle
        for i in range(steps + 1):  # 0 to 100 inclusive
            self.progress = i
            time.sleep(interval)
            bar.update(i)
        print('\n')
        self.setStatus(PlaneStates.InAir)   #Indique que l'avion est dans les airs
        if(self.getCatapult() == "Front"):  #S'il a pris une catapulte a l'avant
            self.semaphoreFront.release()   #Relache la cle semaphore
            if (self.tabCatapultesFront[0] == False): 
                    self.tabCatapultesFront[0] = True  #Indique que la catapulte est maintenant dispo
            elif (self.tabCatapultesFront[1] == False):
                    self.tabCatapultesFront[1] = True
        elif(self.getCatapult() == "Side"): #S'il a pris une catapulte sur le cote
            self.semaphoreSide.release()
            if (self.tabCatapultesSide[0] == False): 
                    self.tabCatapultesSide[0] = True  
            elif (self.tabCatapultesSide[1] == False):
                    self.tabCatapultesSide[1] = True

    #Retourne la valeur actuelle de la barre de progres
    def getProgress(self):
        return self.progress

    #Methode pour faire atterir l'avion
    def landPlane(self):
        #Prend les deux cles du semaphore
        self.semaphoreSide.acquire()
        self.semaphoreSide.acquire()
        #Occupe les deux catapultes du cote
        self.tabCatapultesSide[0] = False
        self.tabCatapultesSide[1] = False

        duration = 20  #En secondes
        steps = 100
        interval = duration / steps  #Temp entre increment

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
            bar.update(i)   #Met a jour la barre de progres
        print('\n')
        self.setStatus(PlaneStates.Retired) #Indique que l'avion est retourne au hangar
        self.semaphoreSide.release()    #relache les cles semaphore
        self.semaphoreSide.release()
        self.tabCatapultesSide[0] = True
        self.tabCatapultesSide[1] = True