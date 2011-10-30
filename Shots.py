import sys, os, pygame
from Global import *
from random import *
from Shot import *
from Util import *

class Shots():
    def __init__(self):
        self.shots = pygame.sprite.OrderedUpdates()

    def newShot(self, xi, yi, xt, yt, type):
        self.shots.add(Shot(xi, yi, xt, yt, type))

    def draw(self, screen):
        #Draw their new positions
        for shot in self.shots:
            shot.draw(screen)

    def clear(self):
        self.shots.empty()