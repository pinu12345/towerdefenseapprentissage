import pygame, Map, os
from Global import *

# Colors
selected    = (  205,   149,   12)

class TowerBar():
    def __init__(self, origX, origY):
        self.towers = [pygame.image.load(os.path.join ('Images\Towers', '1.png')), \
                       pygame.image.load(os.path.join ('Images\Towers', '2.png')), \
                       pygame.image.load(os.path.join ('Images\Towers', '3.png')), \
                       pygame.image.load(os.path.join ('Images\Towers', '4.png')), \
                       pygame.image.load(os.path.join ('Images\Towers', '5.png'))]
        self.origX = origX
        self.origY = origY
        self.space = 16
        self.towerCount = len(self.towers)
        self.selectedTower = 0

    def draw(self, screen):
        for i in range(self.towerCount):
            if i == self.selectedTower-1:
                screen.fill(selected, (self.origX + i * (tileSize + self.space) - 5, self.origY - 5, tileSize + 10, tileSize + 10), 0)
                screen.blit(self.towers[i], (self.origX + i * (tileSize + self.space), self.origY), None, 0)
            else:
                screen.blit(self.towers[i], (self.origX + i * (tileSize + self.space), self.origY), None, 0)

    def onClick(self, pos):
        if (pos[1] > self.origY) and (pos[1] <= self.origY + tileSize):
            x = (pos[0] - self.origX) // (tileSize + self.space)
            if (x >= 0) and (x < self.towerCount) and (pos[0] - self.origX - x * (tileSize + self.space) < tileSize):
                self.selectTower(x+1)

    def selectTower(self, tower):
        self.selectedTower = tower
        self.towers[tower-1] = pygame.image.load(os.path.join ('Images\Towers', str(self.selectedTower)+'.png'))