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
        upgradeX = self.origX + 150
        upgradeY = self.origY + 26
        eraseX = self.origX + 150
        eraseY = self.origY + 64
        if self.selectedTower == -2:
            screen.blit(Images.InterfaceBGbright, (upgradeX, upgradeY) , (upgradeX, upgradeY, tileSize, tileSize), 0)
            screen.blit(Images.InterfaceBGwashed, (eraseX, eraseY) , (eraseX, eraseY, tileSize, tileSize), 0)
        elif self.selectedTower == -3:
            screen.blit(Images.InterfaceBGwashed, (upgradeX, upgradeY) , (upgradeX, upgradeY, tileSize, tileSize), 0)
            screen.blit(Images.InterfaceBGbright, (eraseX, eraseY) , (eraseX, eraseY, tileSize, tileSize), 0)
        else:
            screen.blit(Images.InterfaceBGwashed, (eraseX, eraseY) , (eraseX, eraseY, tileSize, tileSize), 0)
            screen.blit(Images.InterfaceBGwashed, (upgradeX, upgradeY) , (upgradeX, upgradeY, tileSize, tileSize), 0)
            
        for i in range(self.towerCount):
            drawX = self.origX + ((i%(self.towerCount/2)) * (tileSize + self.space)) + 16
            drawY = self.origY + (i/3 * (tileSize + self.space)) + 24
            if i == self.selectedTower:
                screen.blit(Images.InterfaceBGbright, (drawX, drawY) , (drawX, drawY, tileSize, tileSize), 0)
                screen.blit(Images.TowerImages[i][0], (drawX , drawY), None, 0)
            else:
                if i == 4 or i == 1 or i == 2 or i == 3 or i == 0:
                    screen.blit(Images.InterfaceBGwashed, (drawX, drawY) , (drawX, drawY, tileSize, tileSize), 0)
                    screen.blit(Images.TowerImages[i][0], (drawX, drawY), None, 0)
                else:
                    screen.blit(Images.InterfaceBGwashed, (drawX, drawY) , (drawX, drawY, tileSize, tileSize), 0)
                    #screen.blit(Images.TowerImages[i][0], (drawX, drawY), None, 0)
        self.redraw = 0

    def onClick(self, pos):
        #6 Towers
        x = (pos[0] - self.origX - 16) // (tileSize + self.space)
        y = (pos[1] - self.origY - 24) // (tileSize + self.space)
        if (x >= 0) and (x < 3):
            if (y >= 0) and (y < 2):
                self.selectTower(x+(3*y))
        #Upgrade and erase
        elif (pos[0] >= self.origX + 150) and (pos[0] <= self.origY + 178):
            if (pos[1] >= self.origY + 27) and (pos[1] <= self.origY + 54):
                self.selectTower(-2)
            elif (pos[1] >= self.origY + 66) and (pos[1] <= self.origY + 94):
                self.selectTower(-3)

    def selectTower(self, tower):
        self.selectedTower = tower
        self.redraw = 1