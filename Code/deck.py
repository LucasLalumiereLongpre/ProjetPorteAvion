from plane import Plane, PlaneStates
import threading
import time
from multiprocessing import Queue

class Deck:
    def __init__(self, tabCatapultesFront, tabCatapultesSide, semaphoreFront, semaphoreSide, inputQueue):
        self.inputQueue = inputQueue
        self.planes = []   #liste des avons actifs
        self.nbPlanes = 0  #Nb d'avions actifs
        self.threads = []  #Liste qui contient les threads
        self.tabCatapultesFront = tabCatapultesFront
        self.tabCatapultesSide = tabCatapultesSide
        self.semaphoreFront = semaphoreFront
        self.semaphoreSide = semaphoreSide

    def process_input(self):
        if not self.inputQueue.empty():
            return self.inputQueue.get()

    def checkPlanes(self):
        for plane in self.planes:
            print(f"\nPlane {plane.getId()}: {plane.getStatus()}")

    #Verifie si la piste d'aterrisage est disponible
    def checkLanding(self, plane):
        if (self.tabCatapultesSide[0] == True and self.tabCatapultesSide[1] == True): #Si les catapultes du cote sont dispo
            plane.landPlane()
            self.planes.pop(0)
        

    #Fonction qui prepare un avion pour un lancement.
    def prepareToLaunch(self):
        nbPlanes = len(self.planes)
        self.planes.append(Plane(nbPlanes,self.tabCatapultesFront,self.tabCatapultesSide,self.semaphoreFront,self.semaphoreSide))  #Cree un nouvel avion et l'ajoute dans la liste d'avions
        self.planes[nbPlanes].setStatus(PlaneStates.WaitingToLaunch) #met l'etat de l'avion a WaitingToLaunch

        planeThread = threading.Thread(target=self.planes[nbPlanes].launchPlane, name=f"Thread-{nbPlanes + 1}") #Cree un thread pour lancer l'avion
        self.threads.append(planeThread) #Ajoute le thread a la liste de threads
        planeThread.start() #Lance l'avion
    
    def runDeck(self):
        while(True):  
            message = self.process_input()
            if (message is not None):
                print(f"deck: {message}")
            if(message == "l"):     #Pour lancer un avion
                self.prepareToLaunch()
            elif(message == "r"):   #Pour faire atterir un avion
                if self.planes:
                    self.checkLanding(self.planes[0])   #Fait atterir le premier avion dans la liste
                else:
                    print("No planes to land")
            elif(message == "s"):   #Pour afficher les etats des avions
                self.checkPlanes()
            elif(message == "q"):   #Pour fermer le programme
                if self.planes:
                    for plane in self.planes:   #Fait atterir les avions avant de fermer
                        self.checkLanding(plane)
                    for thread in self.threads:
                        thread.join()
                    break
                else:
                    for thread in self.threads:
                        thread.join()
                    break