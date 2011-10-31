import pygame, os, RandomMap
from Game import *
from Util import *
from Util import *
import RandomMap

class Map:
    def __init__(self, mapWidth, mapHeight):

        # This sets the map global parameters
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
        self.showGrid = 0

        # Create a 2 dimensional array. A two dimesional array is simply a list of lists.
        self.M = []
        self.O = []
        self.T = []
        self.currentOX = 0
        self.currentOY = 0
        self.baseX = 0
        self.baseY = 0

        for row in range(self.mapHeight):
            # Add an empty array that will hold each cell in this row
            self.M.append([])
            self.O.append([])
            self.T.append([])
            for column in range(self.mapWidth):
                self.M[row].append(0)
                self.O[row].append(0)
                self.T[row].append(0)
    
    def reset(self):
        # Create a 2 dimensional array. A two dimesional array is simply a list of lists.
        self.M = []
        self.O = []
        self.T = []
        self.currentOX = 0
        self.currentOY = 0
        self.baseX = 0
        self.baseY = 0
        
        for row in range(self.mapHeight):
            # Add an empty array that will hold each cell in this row
            self.M.append([])
            self.O.append([])
            self.T.append([])
            for column in range(self.mapWidth):
                self.M[row].append(0)
                self.O[row].append(0)
                self.T[row].append(0)
    
    def clearTowers(self):
        self.T = []
        for row in range(self.mapHeight):
            self.T.append([])
            for column in range(self.mapWidth):
                self.T[row].append(0)
    
    def loadMap(self, textMap):
        self.reset()
        self.M = textMap
        entrance = findEntrance(self.M)
        self.entranceY = entrance[0][0]
        self.entranceX = entrance[0][1]
        self.entranceDirection = entrance[1]

    def loadTestMap(self):
        self.loadFileMap('testmap')
    
    def loadRandomMap(self):
        self.loadMap(RandomMap.RandomMap().M)
        
    def loadFileMap(self, map_name):
        textMap = open(os.path.join('Maps', map_name+'.txt')).readlines()
        self.loadMap(textMap)