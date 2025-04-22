from plane import Plane, PlaneStates
import threading
import time
import multiprocessing

inputQueue = multiprocessing.Manager().list()  # Shared list for lyrics and blink messages

#sempahores pour catapultes
semaphoreFront = threading.Semaphore(2)
semaphoreSide = threading.Semaphore(2)

#tableaux de catapultes
tabCatapultesFront = [True, True]
tabCatapultesSide = [True, True]

planes = []   #liste des avons actifs
nbPlanes = 0  #Nb d'avions actifs

threads = []  #Liste qui contient les threads

#Verifie si la piste d'aterrisage est disponible
def checkLanding():
    pass

#Fonction qui prepare un avion pour un lancement.
def prepareToLaunch():
    global nbPlanes
    global tabCatapultesFront
    global tabCatapultesSide
    
    nbPlanes = len(planes)
    planes.append(Plane(nbPlanes))  #Cree un nouvel avion et l'ajoute dans la liste d'avions
    planes[nbPlanes].setStatus(PlaneStates.WaitingToLaunch) #met l'etat de l'avion a WaitingToLaunch

    if (tabCatapultesFront[0] == True or tabCatapultesFront[1] == True):  #Si une catapulte en avant est dispo
        semaphoreFront.acquire(blocking=False)  #Prend une cle
        planes[nbPlanes].setCatapult("Front")   #Indique que l'avion est sur une catapulte a l'avant
        if (tabCatapultesFront[0] == True): #Si la catapulte est libre
            tabCatapultesFront[0] = False   #indique que la catpulte n'est plus disponible
        elif (tabCatapultesFront[1] == True):
            tabCatapultesFront[1] = False
    elif (tabCatapultesSide[0] == True or tabCatapultesSide[1] == True): #Si une catapulte sur le cote est dispo
        semaphoreSide.acquire(blocking=False)
        planes[nbPlanes].setCatapult("Side")    #Indique que l'avion est sur une catapulte sur le cote
        if (tabCatapultesSide[0] == True): #Si la catapulte est libre
            tabCatapultesSide[0] = False   #indique que la catpulte n'est plus disponible
        elif (tabCatapultesSide[1] == True):
            tabCatapultesSide[1] = False

    planeThread = threading.Thread(target=planes[nbPlanes].launchPlane, name=f"Thread-{nbPlanes + 1}") #Cree un thread pour lancer l'avion
    threads.append(planeThread) #Ajoute le thread a la liste de threads
    planeThread.start() #Lance l'avion
    
if __name__ == "__main__":
    for i in range(5):
        prepareToLaunch()
        time.sleep(0.1)

    for thread in threads:
        thread.join()
    for plane in planes:
        print(f"\nPlane {plane.getId()}: {plane.getStatus()}")
