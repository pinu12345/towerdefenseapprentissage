import pygame, Map, os, Images
from Global import *

# Colors
selected = (205, 149, 12)

class TowerBar():
    def __init__(self, origX, origY):
        self.origX = origX
        self.origY = origY
        self.space = 16
        self.towerCount = len(Images.TowerImages)
        self.selectedTower = 0
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
        print('Redrawing towerBar')
        for i in range(self.towerCount):
            if i == self.selectedTower-1:
                screen.fill(selected, (self.origX + i * (tileSize + self.space) - 5, self.origY - 5, tileSize + 10, tileSize + 10), 0)
                screen.blit(Images.TowerImages[i][0], (self.origX + i * (tileSize + self.space), self.origY), None, 0)
            else:
                screen.blit(Images.InterfaceBG, (self.origX + i * (tileSize + self.space) - 5, self.origY - 5) , (self.origX + i * (tileSize + self.space) - 5, self.origY - 5, tileSize + 10, tileSize + 10), 0)
                screen.blit(Images.TowerImages[i][0], (self.origX + i * (tileSize + self.space), self.origY), None, 0)
        self.redraw = 0

    def onClick(self, pos):
        if (pos[1] > self.origY) and (pos[1] <= self.origY + tileSize):
            x = (pos[0] - self.origX) // (tileSize + self.space)
            if (x >= 0) and (x < self.towerCount) and (pos[0] - self.origX - x * (tileSize + self.space) < tileSize):
                self.selectTower(x+1)

    def selectTower(self, tower):
        self.selectedTower = tower
        self.redraw = 1