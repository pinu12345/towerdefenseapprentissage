import pygame, Map, os

class TowerBar():
    def __init__(self, origX, origY):
        self.towers = [pygame.image.load(os.path.join ('Images\Towers', '1.png')),\
                       pygame.image.load(os.path.join ('Images\Towers', '2.png')),\
                       pygame.image.load(os.path.join ('Images\Towers', '3.png')),\
                       pygame.image.load(os.path.join ('Images\Towers', '4.png')),\
                       pygame.image.load(os.path.join ('Images\Towers', '5.png'))]
        self.origX = origX
        self.origY = origY
        self.towerSize = 32
        self.space = 16
        self.towerCount = len(self.towers)
        self.selectedTower = 0
    
    def draw(self, screen):
        for i in range(self.towerCount):
            screen.blit(self.towers[i], (self.origX + i * (self.towerSize + self.space), self.origY))

    def onClick(self, pos):
        print("Coords:",pos[0],",",pos[1])
        if (pos[1] > self.origY) and (pos[1] <= self.origY + self.towerSize):
            x = (pos[0] - self.origX) // (self.towerSize + self.space)
            if (x >= 0) and (x < self.towerCount) and (pos[0] - self.origX - x * (self.towerSize + self.space) < self.towerSize):
                self.selectedTower = x+1
                self.towers[x] = pygame.image.load(os.path.join ('Images\Towers', str(self.selectedTower)+'.png'))