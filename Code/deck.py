from plane import Plane, PlaneStates
import threading
import time
from multiprocessing import Queue

#sempahores pour catapultes
semaphoreFront = threading.Semaphore(2)
semaphoreSide = threading.Semaphore(2)

#tableaux de catapultes
tabCatapultesFront = [True, True]
tabCatapultesSide = [True, True]

planes = []   #liste des avons actifs
nbPlanes = 0  #Nb d'avions actifs

threads = []  #Liste qui contient les threads

def process_input(inputQueue):
    if not inputQueue.empty():
        return inputQueue.get()

def checkPlanes():
    for plane in planes:
        print(f"\nPlane {plane.getId()}: {plane.getStatus()}")

#Verifie si la piste d'aterrisage est disponible
def checkLanding(plane):
    if (tabCatapultesSide[0] == True and tabCatapultesSide[1] == True): #Si les catapultes du cote sont dispo
        #Prend les deux cles du semaphore
        semaphoreSide.acquire(blocking=False)
        semaphoreSide.acquire(blocking=False)
        tabCatapultesFront[0] = False
        tabCatapultesFront[1] = False
        plane.landPlane()
    

#Fonction qui prepare un avion pour un lancement.
def prepareToLaunch():
    global nbPlanes
    global tabCatapultesFront
    global tabCatapultesSide
    
    nbPlanes = len(planes)
    planes.append(Plane(nbPlanes))  #Cree un nouvel avion et l'ajoute dans la liste d'avions
    planes[nbPlanes].setStatus(PlaneStates.WaitingToLaunch) #met l'etat de l'avion a WaitingToLaunch

    planeThread = threading.Thread(target=planes[nbPlanes].launchPlane, name=f"Thread-{nbPlanes + 1}") #Cree un thread pour lancer l'avion
    threads.append(planeThread) #Ajoute le thread a la liste de threads
    planeThread.start() #Lance l'avion
    
if __name__ == "__main__":
    inputQueue = Queue()

    while(process_input(inputQueue) != 'q'):    #Pour lancer un avion
        message = process_input()
        if(message == 'l'):
            prepareToLaunch()
        elif(message == 'r'):   #Pour faire atterir un avion
            if planes:
                checkLanding(planes[0])
            else:
                print("No planes to land")
        elif(message == 's'):   #Pour afficher les etats des avions
            checkPlanes()