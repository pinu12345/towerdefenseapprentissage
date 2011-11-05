import sys, os, pygame, Enemy, Game
from Global import *
from random import *
from Util import *

class Level():
    def __init__(self, levelName):
        self.waves = []
        self.map = []
        
        self.money = 100
        self.waves.append(0, 10)
        self.waves.append(1, 5)
        self.waves.append(2, 10)
        
        self.levelText = open(os.path.join('Levels', levelName+'.txt')).readlines()
        self.map = self.levelText
        
    def sendWave(self):
        #if wave is over reset tower cooldowns, and start the new wave
        pass
    
    