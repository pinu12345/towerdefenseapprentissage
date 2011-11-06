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
        addedTower = Tower.Tower(row, column, towerType-1, self.map)
        self.towers.add(addedTower)
        map.T[row][column] = addedTower

    def updateTower(self, map, towerType, row, column):
        currentTower = map.T[row][column]
        if towerType-1 == currentTower.type:
            currentTower.upgrade()
        else:
            currentTower.resetEmplacement()
            currentTower.kill()
            addedTower = Tower.Tower(row, column, towerType-1, self.map)
            self.towers.add(addedTower)
            map.T[row][column] = addedTower

    def target(self, shots):
        for tower in self.towers:
            tower.target(self.wave.enemies, shots)

    def draw(self, screen):
        for tower in self.towers:
            tower.draw(screen)
    
    def clear(self):
        Game.placedTower = 1
        self.map.clearTowers()
        for tower in self.towers:
            tower.resetEmplacement()
        self.towers.empty()