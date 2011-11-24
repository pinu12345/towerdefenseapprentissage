import pygame, os, RandomMap
from Game import *
from Util import *
from Global import *

class Map:
    def __init__(self, mapWidth, mapHeight):

        self.S = []
        self.M = []
        self.O = []
        self.T = []
        self.P = []
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
                self.O[row].append(-1)
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
                self.O[row].append(-1)
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
        mapSeed = 0
        for row in textMap:
            for tile in row:
                if tile == car_path:
                    mapSeed += 1
        random.seed(mapSeed)
        for row in range(mapHeight):
            self.S.append([])
            for column in range(mapWidth):
                type = self.orientTile(column, row)
                if type == ROUTEH:
                    flipX = random.randint(0, 2)
                    flipY = random.randint(0, 2)
                    if randint(0, 4):
                        randNum = 0
                    else:
                        randNum = random.randint(len(Images.MapImages[MAPROUTE]))
                    randImage = Images.MapImages[MAPROUTE][randNum]
                    randImage = pygame.transform.flip(randImage, flipX, flipY)
                    self.S[row].append(randImage)
                elif type == ROUTEV:
                    flipX = random.randint(0, 2)
                    flipY = random.randint(0, 2)
                    if randint(0, 4):
                        randNum = 0
                    else:
                        randNum = random.randint(len(Images.MapImages[MAPROUTE]))
                    randImage = pygame.transform.rotate( \
                        Images.MapImages[MAPROUTE][randNum], 90)
                    randImage = pygame.transform.flip(randImage, flipX, flipY)
                    self.S[row].append(randImage)
                elif type in [ROUTENW, ROUTENE, ROUTESW, ROUTESE]:
                    flipXY = random.randint(0, 2)
                    if flipXY:
                        rotFlip = 180
                    else:
                        rotFlip = 0
                    if choice([0, 1]):
                        randNum = 0
                    else:
                        randNum = random.randint(len(Images.MapImages[MAPROUTTURN]))
                    if type == ROUTENW:
                        rotType = 90
                    elif type == ROUTENE:
                        rotType = 0
                    elif type == ROUTESE:
                        rotType = -90
                    elif type == ROUTESW:
                        rotType = 180
                    randImage = pygame.transform.flip( \
                        Images.MapImages[MAPROUTTURN][randNum], flipXY, flipXY)
                    randImage = pygame.transform.rotate(randImage, rotType + rotFlip)
                    self.S[row].append(randImage)
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
                    flipX = random.randint(0, 2)
                    flipY = random.randint(0, 2)
                    randRot = 90*random.randint(0, 4)
                    if randint(0, 2):
                        randNum = 0
                    else:
                        randNum = random.randint(len(Images.MapImages[MAPWASTELAND]))
                    
                    randImage = Images.MapImages[MAPWASTELAND][randNum]
                    randImage = pygame.transform.rotate(randImage, randRot)
                    randImage = pygame.transform.flip(randImage, flipX, flipY)
                    self.S[row].append(randImage)
        random.seed()
        
        #print '\n Generating precise path map...'
        #self.P = precisePathMap(self.M)
        #print ' Done.\n'
        #print len(P), len(P[0])
        #print
        #stepSize = 16
        #carPathCount = 0
        #for i in range(0, len(self.P), stepSize):
        #    temp = [' ']
        #    for j in range(0, len(self.P[0]), stepSize):
        #        temp.append(self.P[i][j])
        #        if self.P[i][j] == car_path:
        #            carPathCount += 1
        #    print ''.join(temp)
        #print '', carPathCount, '\n'
        
        entrance = findEntrance(self.M)
        self.entranceY = entrance[0][0]
        self.entranceX = entrance[0][1]
        self.entranceDirection = entrance[1]

    def loadBasicMap(self):
        self.loadFileMap('basicmap')
    
    def loadRandomMap(self):
        self.loadMap(RandomMap.RandomMap().M)
        
    def loadFileMap(self, map_name):
        textMap = open(os.path.join('Maps', map_name+'.txt')).readlines()
        #print textMap
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