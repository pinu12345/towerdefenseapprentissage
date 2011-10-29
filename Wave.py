import sys, os, pygame, Enemy
from Global import *
from random import *
from Util import *

class Wave():
    def __init__(self, map):
        self.spawnType = 0
        self.spawnCount = 0
        self.spawnTimer = 0
        self.spawnDelay = 0
        self.map = map
        self.enemies = pygame.sprite.OrderedUpdates()
        self.newRandomSpawn()

    def newSpawn(self, type, count):
        self.spawnType = type
        self.spawnCount = count
        self.spawnDelay = EnemyTypes[self.spawnType][EnemyDELAY] * 100 / EnemyTypes[self.spawnType][EnemySPEED]
        self.spawnTimer = spawnDelay

    def spawn(self):
        self.spawnTimer += 1
        if self.spawnTimer >= self.spawnDelay:
            self.spawnTimer = 0
            if self.spawnCount > 0:
                self.spawnCount = self.spawnCount - 1
                self.enemies.add(Enemy.Enemy(self.spawnType, self, self.map.entranceX, self.map.entranceY, self.map.entranceDirection, self.spawnCount))
            else:
                pass

    def move(self):
        #Move the enemies
        for enemy in self.enemies:
            enemy.move()

    def draw(self, screen):
        #Draw their new positions
        for enemy in self.enemies:
            enemy.draw(screen)
    
    def newRandomSpawn(self):
        self.newSpawn(randint(0,4), randint(75, 100))
        
    def clear(self):
        self.enemies.empty()
        self.spawnTimer = 0
        self.spawnCount = 0
        self.spawnType = 0
        self.spawnDelay = 0