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

    #Fonction pour recevoir une commande
    def process_input(self):
        if not self.inputQueue.empty(): #S'il y a une commande dans la queue
            return self.inputQueue.get()

    #Fonction qui retourne le status des avions
    def checkPlanes(self):
        for plane in self.planes:
            print(f"\nPlane {plane.getId()}: {plane.getStatusName()}")

    #Verifie si la piste d'aterrisage est disponible
    def checkLanding(self, plane):
        if (self.tabCatapultesSide[0] == True and self.tabCatapultesSide[1] == True): #Si les catapultes du cote sont dispo
            landingThread = threading.Thread(target=plane.landPlane)
            self.threads.append(landingThread) #Ajoute le thread a la liste de threads
            landingThread.start()   #Part un thread pour atterir un avion
        

    #Fonction qui prepare un avion pour un lancement.
    def prepareToLaunch(self):
        nbPlanes = len(self.planes)
        self.planes.append(Plane(nbPlanes,self.tabCatapultesFront,self.tabCatapultesSide,self.semaphoreFront,self.semaphoreSide))  #Cree un nouvel avion et l'ajoute dans la liste d'avions
        self.planes[nbPlanes].setStatus(PlaneStates.WaitingToLaunch) #met l'etat de l'avion a WaitingToLaunch

        planeThread = threading.Thread(target=self.planes[nbPlanes].launchPlane, name=f"Thread-{nbPlanes + 1}") #Cree un thread pour lancer l'avion
        self.threads.append(planeThread) #Ajoute le thread a la liste de threads
        planeThread.start() #Lance l'avion
    
    #Fonction pour operer le deck
    def runDeck(self):
        while(True):    #Boucle principale
            message = self.process_input()  #recoit un message de la tour de controle
            if (message is not None):
                print(f"deck: {message}")
            if(message == "l"):     #Pour lancer un avion
                self.prepareToLaunch()
            elif(message == "r"):   #Pour faire atterir un avion
                if self.planes:
                    for plane in self.planes:
                        if (plane.getStatus() == PlaneStates.InAir):
                            self.checkLanding(plane)   #Fait atterir le premier avion qui vole dans la liste
                            break
                else:
                    print("No planes to land")
            elif(message == "s"):   #Pour afficher les etats des avions
                self.checkPlanes()
            elif(message == "q"):   #Pour fermer le programme
                if self.planes:
                    for plane in self.planes:   #Fait atterir les avions avant de fermer
                        if (plane.getStatus() == PlaneStates.InAir):
                            self.checkLanding(plane)    #Fait atterir tous les avions dans les airs
                    for thread in self.threads:
                        thread.join()   #Attend que tous les threads se ferment
                    break   #Sort de la boucle while
                else:
                    for thread in self.threads:
                        thread.join()
                    break