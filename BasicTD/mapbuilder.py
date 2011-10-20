import pygame, os
from startup import *

class Map:
    def __init__(self, map, background):
        """This is all the map data, paramaters are map file name"""

        #only parameters to be passed should be easy or hard
        self.mapFileName = os.path.join ('data', map + 'map.txt')
        self.linesList = None
        self.wayPoint = None
        self.charList = None

        #load up the tiles image
        tiles = pygame.image.load(os.path.join('data', 'tiles.png'))
        self.sidebar = pygame.image.load(os.path.join('data', 'sidebar.png'))
        self.TILESIZE = 25

        self.displayMap = pygame.display.get_surface()

        #set the image of each tile image
        self.imgList = []

        imgSize = (25, 25)
        offset = ((0,0), (0,25), (25,0), (25,25))

        for i in range(4):
            tmpImg = pygame.Surface(imgSize)
            tmpImg.blit(tiles, (0, 0), (offset[i], imgSize))
            self.imgList.append(tmpImg)

    def buildMap(self):
        """Reads the map and sets it up for display"""
        file = open(self.mapFileName, 'r')
        self.linesList = file.readlines()
        self.charList = self.linesList

        for i in range(len(self.linesList)):
            self.linesList[i] = self.linesList[i].strip()#remove whitespace
            for j in range(len(self.linesList[i])):

                #load the appropriate image for this ASCII character
                tile = self.loadTile(self.linesList[i][j], i, j)

                #now put it on the window in the appropriate place
                tileRect = tile.get_rect()#get the bounding rectangle

                #move the rectangle to the appropriate x,y location on the window
                tileRect.left = self.TILESIZE*j
                tileRect.top = self.TILESIZE*i

                #put this tile on the hidden updated canvas in the correct place
                self.displayMap.blit(tile, tileRect)

        sidebarRect = self.sidebar.get_rect()
        sidebarRect.topleft = (625,0)
        self.displayMap.blit(self.sidebar,sidebarRect)

    def loadTile(self, char, i, j):
        """Trying to figure a way to use tiled images,
        Dont want to access filesystem 100 + times"""

        if char == 'E':
            image = self.imgList[0]
            self._E = (self.TILESIZE*j+12,self.TILESIZE*i+12)
        elif char == 'G':
            image = self.imgList[1]
        elif char == 'S':
            image = self.imgList[2]
            self._S = (self.TILESIZE*j+12,self.TILESIZE*i+12)
        elif char == 'P' or range(0,9):
            image = self.imgList[3]
        elif char == 'a':
            image = self.imgList[4]

        #Get the center of each of the corner tiles
        if char == '0':
            self._0 = (self.TILESIZE*j+12,self.TILESIZE*i+12)
        elif char == '1':
            self._1 = (self.TILESIZE*j+12,self.TILESIZE*i+12)
        elif char == '2':
            self._2 = (self.TILESIZE*j+12,self.TILESIZE*i+12)
        elif char == '3':
            self._3 = (self.TILESIZE*j+12,self.TILESIZE*i+12)
        elif char == '4':
            self._4 = (self.TILESIZE*j+12,self.TILESIZE*i+12)
        elif char == '5':
            self._5 = (self.TILESIZE*j+12,self.TILESIZE*i+12)
        elif char == '6':
            self._6 = (self.TILESIZE*j+12,self.TILESIZE*i+12)
        elif char == '7':
            self._7 = (self.TILESIZE*j+12,self.TILESIZE*i+12)
        elif char == '8':
            self._8 = (self.TILESIZE*j+12,self.TILESIZE*i+12)
        elif char == '9':
            self._9 = (self.TILESIZE*j+12,self.TILESIZE*i+12)
        return image

    def getGrid(self):
        return self.charList

    def checkWaypoints(self):
        """Returns the list of the waypoints' Coordinates of their center"""
        #set up the code to take the waypoints from self.waypoint
        self.wayPoint = [self._S, self._E, self._0, self._1,
                        self._2, self._3, self._4, self._5,
                        self._6, self._7, self._8, self._9]
        return self.wayPoint

class GridControl:
    def __init__(self, map, screen, grid):
        self.charList = grid
        self.TILESIZE = 25
        self.surf = pygame.Surface((self.TILESIZE,self.TILESIZE))
        self.m_x = -100
        self.m_y = -100
        self.C_red = (255,0,0)
        self.C_green = (0,255,0)
        self.C_yellow = (255,255,0)
        self.C_empty = (0,0,0)
        self.chosenColor = self.C_empty
        self.surf.set_alpha(255*0.4)
        self.surf.fill(self.chosenColor)
        self.doubleClik = 2
        self.clickLocX = -1000
        self.clickLocY = -1000

    def click(self):
        self.doubleClik = 2
        mux, muy = pygame.mouse.get_pos()
        self.clickLocX = mux/self.TILESIZE
        self.clickLocY = muy/self.TILESIZE
        self.m_x = self.clickLocX*self.TILESIZE
        self.m_y = self.clickLocY*self.TILESIZE

        if (self.m_x < 625) and (self.m_y < 625):
            tile = self.checkTile(self.charList[self.clickLocY][self.clickLocX])
            self.chosenColor = tile

        self.surf.fill(self.chosenColor)

    def unclick(self):
        self.doubleClik -= 1
        if self.doubleClik == 0:
            self.m_x = -100
            self.m_y = -100
            self.chosenColor = self.C_empty

    def checkTile(self, char):

        if char == 'G':
            return self.C_green
        elif char =='T':
            return self.C_yellow
        else:
            return self.C_red

    def setTower(self):
        if (self.chosenColor == self.C_green):
            changeChar = list(self.charList[self.clickLocY])
            changeChar[self.clickLocX] = 'T'
            changeChar = "".join(changeChar)
            self.charList[self.clickLocY] = changeChar
            self.chosenColor = self.C_yellow
            self.surf.fill(self.chosenColor)
            return (self.m_x, self.m_y)

    def removeTower(self):
        if (self.chosenColor == self.C_yellow):
            changeChar = list(self.charList[self.clickLocY])
            changeChar[self.clickLocX] = 'G'
            changeChar = "".join(changeChar)
            self.drawSelection()
            self.charList[self.clickLocY] = changeChar
            self.chosenColor = self.C_green
            self.surf.fill(self.chosenColor)

    def checkTower(self):
        if self.chosenColor != self.C_empty:
            tile = self.checkTile(self.charList[self.clickLocY][self.clickLocX])
            if tile == self.C_green:
                return 'No'
            else:
                return 'Yes'