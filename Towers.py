import sys, os, pygame, Enemy, Tower
from Global import *
from random import *
from Util import *

class Towers():
    def __init__(self, map, wave):
        self.map = map
        self.towers = pygame.sprite.Group()
        self.wave = wave

    def placeTower(self, map, towerType, row, column):
        map.T[row][column] = towerType
        self.towers.add(Tower.Tower(row, column, towerType-1))

    def target(self, shots):
        for tower in self.towers:
            tower.target(self.wave.enemies, shots)

    def draw(self, screen):
        self.towers.draw(screen)
    
    def clear(self):
        self.map.clearTowers()
        self.towers.empty()