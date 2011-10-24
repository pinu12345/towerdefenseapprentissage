import sys, os, pygame, Enemy, Tower
from Global import *
from random import *
from Util import *

class Towers():
    def __init__(self, map):
        self.map = map
        self.towers = pygame.sprite.Group()

    def placeTower(self, map, towerType, row, column):
        map.T[row][column] = towerType
        self.towers.add(Tower.Tower(row, column, towerType-1))
    
    def removeTower(self, tower):
        #If the game is not started yet
        #Destroy the tower
        tower.kill()
        #Refund the price
        pass

    def draw(self, screen):
        self.towers.draw(screen)