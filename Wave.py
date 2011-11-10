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
        Game.enemyCount = 0
        self.map = map
        self.enemies = pygame.sprite.OrderedUpdates()

    def newSpawn(self, type, count):
        self.spawnType = type
        self.spawnCount = count
        Game.enemyCount = count
        self.spawnDelay = EnemyStats[self.spawnType][EnemySPREAD] \
            / EnemyStats[self.spawnType][EnemySPEED]
        self.spawnTimer = self.spawnDelay

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
        randType = randint(0, 8)
        self.newSpawn(randType, \
            max(1, randint(10, 100)**2/EnemyStats[randType][EnemyVALUE]))

    def clear(self):
        Game.enemyCount = 0
        self.enemies.empty()
        self.spawnTimer = 0
        self.spawnCount = 0
        self.spawnType = 0
        self.spawnDelay = 0