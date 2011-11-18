import pygame, Map, os, Images
from Global import *

# Colors
selected = (205, 149, 12)

class TowerBar():
    def __init__(self, origX, origY):
        self.origX = origX
        self.origY = origY
        self.space = 8
        self.towerCount = len(Images.TowerImages)
        self.selectedTower = -1
        self.redraw = 1

    # Update les graphiques
    #  Fill la tour precedente de noir et la redessine par dessu
    #  Fill la nouvelle tour en or et la redessine par dessu
    def update(self, screen):
        self.previousSelected = self.selectedTower

    # Dessine les tours dans la barre
    #  Si une tour est selectionner dessine un arriere plan en or
    #  Sinon dessine un arriere plan noir
    def draw(self, screen):
        #print('Redrawing towerBar')
        for i in range(self.towerCount):
            drawX = self.origX + ((i%(self.towerCount/2)) * (tileSize + self.space))
            drawY = self.origY + (i/3 * (tileSize + self.space))
            if i == self.selectedTower:
                screen.blit(Images.InterfaceBGbright, (drawX, drawY) , (drawX, drawY, tileSize, tileSize), 0)
                screen.blit(Images.TowerImages[i][0], (drawX , drawY), None, 0)
            else:
                if i == 4 or i == 1 or i == 2 or i == 3 or i == 0:
                    screen.blit(Images.InterfaceBGopaque, (drawX, drawY) , (drawX, drawY, tileSize, tileSize), 0)
                    screen.blit(Images.TowerImages[i][0], (drawX, drawY), None, 0)
                else:
                    screen.blit(Images.InterfaceBGwashed, (drawX, drawY) , (drawX, drawY, tileSize, tileSize), 0)
                    #screen.blit(Images.TowerImages[i][0], (drawX, drawY), None, 0)
        self.redraw = 0

    def onClick(self, pos):
        x = (pos[0] - self.origX) // (tileSize + self.space)
        y = (pos[1] - self.origY) // (tileSize + self.space)
        if (x >= 0) and (x < 3):
            if (y >= 0) and (y < 2):
                self.selectTower(x+(3*y))

    def selectTower(self, tower):
        self.selectedTower = tower
        self.redraw = 1