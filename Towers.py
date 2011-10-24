import sys, os, pygame, Enemy
from Global import *
from random import *
from Util import *

class Wave():
    def __init__(self, map):
        self.map = map
        self.towers = pygame.sprite.Group()

    def placeTower(self, tower):
        #self.towers.add()
        pass
    
    def removeTower(self, tower):
        #If the game is not started yet
        #Destroy the tower
        tower.kill()
        #Refund the price
        pass

    def draw(self, screen):
        self.towers.draw(screen)