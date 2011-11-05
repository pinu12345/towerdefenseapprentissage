import pygame, os, RandomMap
from Game import *
from Util import *
from Global import *
import RandomMap

class Map:
    def __init__(self, mapWidth, mapHeight):

        self.S = []
        self.M = []
        self.O = []
        self.T = []
        self.currentOX = 0
        self.currentOY = 0
        self.baseX = 0
        self.baseY = 0

        for row in range(mapHeight):
            # Add an empty array that will hold each cell in this row
            self.M.append([])
            self.O.append([])
            self.T.append([])
            for column in range(mapWidth):
                self.M[row].append(0)
                self.O[row].append(0)
                self.T[row].append(0)
    
    def reset(self):
        self.S = []
        self.M = []
        self.O = []
        self.T = []
        self.currentOX = 0
        self.currentOY = 0
        self.baseX = 0
        self.baseY = 0
        
        for row in range(mapHeight):
            # Add an empty array that will hold each cell in this row
            self.M.append([])
            self.O.append([])
            self.T.append([])
            for column in range(mapWidth):
                self.M[row].append(0)
                self.O[row].append(0)
                self.T[row].append(0)
    
    def clearTowers(self):
        self.T = []
        for row in range(mapHeight):
            self.T.append([])
            for column in range(mapWidth):
                self.T[row].append(0)
    
    def loadMap(self, textMap):
        self.reset()
        self.M = textMap
        self.S = []
        for row in range(mapHeight):
            self.S.append([])
            for column in range(mapWidth):
                type = self.orientTile(column, row)
                if type == ROUTEH:
                #MAPROUTE = 0
                #MAPROUTTURN = 1
                #MAPEMPLACEMENT = 2
                #MAPBASE = 3
                #MAPWASTELAND = 4
                    self.S[row].append(Images.MapImages[MAPROUTE][0])
                elif type == ROUTEV:
                    self.S[row].append(pygame.transform.rotate(Images.MapImages[MAPROUTE][0],90))
                elif type == ROUTENW:
                    self.S[row].append(pygame.transform.rotate(Images.MapImages[MAPROUTTURN][0],90))
                elif type == ROUTENE:
                    self.S[row].append(Images.MapImages[MAPROUTTURN][0])
                elif type == ROUTESE:
                    self.S[row].append(pygame.transform.rotate(Images.MapImages[MAPROUTTURN][0],270))
                elif type == ROUTESW:
                    self.S[row].append(pygame.transform.rotate(Images.MapImages[MAPROUTTURN][0],180))
                elif type == BASEN:
                    self.S[row].append(pygame.transform.rotate(Images.MapImages[MAPBASE][0],270))
                elif type == BASES:
                    self.S[row].append(pygame.transform.rotate(Images.MapImages[MAPBASE][0],90))
                elif type == BASEE:
                    self.S[row].append(pygame.transform.rotate(Images.MapImages[MAPBASE][0],180))
                elif type == BASEW:
                    self.S[row].append(Images.MapImages[MAPBASE][0])
                elif type == EMPLACEMENT:
                    self.S[row].append(Images.MapImages[MAPEMPLACEMENT][0])
                elif type == WASTELAND:
                    self.S[row].append(Images.MapImages[MAPWASTELAND][0])
                    

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

    def orientTile(self, x, y):
        if self.M[y][x] == car_turret:
            return EMPLACEMENT
        elif self.M[y][x] == car_empty:
            return WASTELAND
        elif x in [0, mapWidth-1]:
            return ROUTEH
        elif y in [0, mapHeight-1]:
            return ROUTEV
        else:
            car_pb = [car_path, car_base]
            if self.M[y][x-1] in car_pb:
                if self.M[y][x+1] in car_pb:
                    return ROUTEH
                elif self.M[y-1][x] in car_pb:
                    return ROUTENW
                elif self.M[y+1][x] in car_pb:
                    return ROUTESW
                else:
                    return BASEW
            elif self.M[y][x+1] in car_pb:
                if self.M[y-1][x] in car_pb:
                    return ROUTENE
                elif self.M[y+1][x] in car_pb:
                    return ROUTESE
                else:
                    return BASEE
            elif self.M[y-1][x] in car_pb:
                if self.M[y+1][x] in car_pb:
                    return ROUTEV
                else:
                    return BASEN
            else:
                return BASES