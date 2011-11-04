import pygame, os, RandomMap
from Game import *
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

    def drawAt(self, layer, color, row, column):
        # Draw tiles with Grid
        if self.showGrid == 1:
            pygame.draw.rect(layer, color, [tileSize*column, tileSize*row, tileSize-gridSize, tileSize-gridSize])
        # Draw tiles without grid
        else:
            pygame.draw.rect(layer, color, [tileSize*column, tileSize*row, tileSize, tileSize])
            
    def orientTile(self, x, y):
        if x in [0, mapWidth-1]:
            return ROUTEH
        elif y in [0, mapHeight-1]:
            return ROUTEV
        else:
            car_pb = [car_path, car_base]
            if self.M[y, x-1] in car_pb:
                if self.M[y, x+1] in car_pb:
                    return ROUTEH
                elif self.M[y-1, x] in car_pb:
                    return ROUTENW
                elif self.M[y+1, x] in car_pb:
                    return ROUTESW
                else:
                    return BASEW
            elif self.M[y, x+1] in car_pb:
                if self.M[y-1, x] in car_pb:
                    return ROUTENE
                elif self.M[y+1, x] in car_pb:
                    return ROUTESE
                else:
                    return BASEE
            elif self.M[y-1, x] in car_pb:
                if self.M[y+1, x] in car_pb:
                    return ROUTEV
                else:
                    return BASEN
            else:
                return BASES
                
        
        