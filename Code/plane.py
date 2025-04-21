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

    def getId(self):
        return self.id
    
    def getStatus(self):
        return self.status
    
    def setStatus(self, status):
        self.status = status

    def launchPlane(self):
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
        
        self.setStatus(PlaneStates.Launching)
        for i in range(steps + 1):  # 0 to 100 inclusive
            self.progress = i
            time.sleep(interval)
            bar.update(i)
        self.setStatus(PlaneStates.InAir)

    def getProgress(self):
        return self.progress
