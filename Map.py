import pygame, os, RandomMap
from Game import *
import RandomMap

class Map:
    def __init__(self, mapWidth, mapHeight):

        # This sets the map global parameters
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
        self.showGrid = 0
        
        # This sets the margin between each cell
        self.margin = 1

        # Create a 2 dimensional array. A two dimesional array is simply a list of lists.
        self.M = []
        self.O = []
        self.T = []
        self.currentOX = 0
        self.currentOY = 0

        for row in range(self.mapHeight):
            # Add an empty array that will hold each cell in this row
            self.M.append([])
            self.O.append([])
            self.T.append([])
            for column in range(self.mapWidth):
                self.M[row].append(0)
                self.O[row].append(0)
                self.T[row].append(0)
    
    def loadMap(self, textMap):
        car_empty, car_path, car_turret, car_base = '-', 'X', 'O', 'B'
        for i in range(len(textMap)):
            for j in range(len(textMap[0])):
				if textMap[i][j] == car_path:
					self.M[i][j] = 1
				elif textMap[i][j] == car_turret:
					self.M[i][j] = 2
				elif textMap[i][j] == car_base:
					self.M[i][j] = 3

    def loadBasicMap(self):
        self.M[5][0] = 1
        self.M[5][1] = 1
        self.M[5][2] = 1
        self.M[5][3] = 1
        self.M[5][4] = 1
        self.M[6][3] = 2
        self.M[6][4] = 1
        self.M[7][4] = 1
        self.M[8][4] = 1
        self.M[9][4] = 1
        self.M[10][4] = 1
        self.M[10][5] = 1
        self.M[10][6] = 1
        self.M[10][7] = 1
        self.M[10][8] = 1
        self.M[10][9] = 1
        self.M[9][9] = 1
        self.M[8][9] = 1
        self.M[7][9] = 1
        self.M[6][9] = 1
        self.M[6][10] = 1
        self.M[6][11] = 1
        self.M[6][12] = 1
        self.M[6][13] = 1
        self.M[6][14] = 1
        self.M[7][14] = 1
        self.M[8][14] = 1
        self.M[8][13] = 1
        self.M[8][12] = 1
        self.M[9][12] = 1
        self.M[9][13] = 2
        self.M[10][12] = 1
        self.M[10][13] = 1
        self.M[10][14] = 1
        self.M[10][15] = 1
        self.M[10][16] = 1
        self.M[10][17] = 1
        self.M[10][18] = 1
        self.M[11][18] = 1
        self.M[12][18] = 1
        self.M[12][19] = 1
        self.M[12][20] = 1
        self.M[12][21] = 1
        self.M[11][21] = 1
        self.M[10][21] = 1
        self.M[9][21] = 1
        self.M[8][21] = 1
        self.M[7][21] = 1
        self.M[7][22] = 1
        self.M[7][23] = 1
        self.M[6][23] = 2

    def loadTestMap(self):
        self.loadFileMap('testmap')
    
    def loadRandomMap(self):
        self.loadMap(RandomMap.RandomMap().M)
        
    def loadFileMap(self, map_name):
        textMap = open(os.path.join('Maps', map_name+'.txt')).readlines()
        self.loadMap(textMap.strip('\n'))