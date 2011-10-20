import pygame, os
from Game import *

type = 0

class Enemy(pygame.sprite.Sprite):
    def __init__(type):
        self.type = type
        pygame.image.load(os.path.join ('Images\Enemies', str(self.type)+'.png'))
        
    def move(self):
        pass
    
    def update(self):
        pass