import sys, os, pygame, Enemy
from Global import *
from random import *

class Wave():
    def __init__(self, map):
        self.tileSize = 33
        
        self.spawnType = 0
        self.spawnCount = 0
        self.spawnTimer = 0
        self.spawnDelay = 0
        self.map = map
        
        self.newSpawn(randint(0,4), randint(5,10))
        
        self.enemies = pygame.sprite.Group()

    def newSpawn(self, type, count):
        self.spawnType = type
        self.spawnCount = count
        self.spawnDelay = EnemyTypes[self.spawnType][EnemyDELAY]
    
    def spawn(self):
        self.spawnTimer += 1
        if self.spawnTimer == self.spawnDelay:
            self.spawnTimer = 0
            if self.spawnCount > 0:
                self.spawnCount = self.spawnCount - 1
                self.enemies.add(Enemy.Enemy(self.spawnType, self, self.map.baseX, self.map.baseY))
            else:
                self.newSpawn(randint(4,4), randint(5,10))
        
    def draw(self, screen):
        #Move the enemies
        for enemy in self.enemies:
            enemy.move(1)
        #Draw their new positions
        self.enemies.draw(screen)