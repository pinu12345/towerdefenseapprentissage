import pygame, os, random
from Game import *
from Global import *

type = 0

class Enemy(pygame.sprite.Sprite):
    def __init__(self, type, wave, x, y):
        
        # Set the enemy type
        self.type = type
        self.wave = wave

        # Set the enemy parameters
        self.name = EnemyTypes[self.type][EnemyNAME]
        self.value = EnemyTypes[self.type][EnemyVALUE]
        self.hp = EnemyTypes[self.type][EnemyHP]
        self.armor = EnemyTypes[self.type][EnemyARMOR]
        self.speed = EnemyTypes[self.type][EnemySPEED]
        
        # Required by Sprite
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join ('Images\Enemies', str(self.type)+'.png'))
        self.rect = self.image.get_rect()

        # Initialize position
        self.setPosition(x, y)

    def move(self, direction):
        if self.rect.x > 800:
            self.kill()
        self.rect.x += self.speed

    def update(self):
        pass

    def setPosition(self, x, y):
        self.rect.x = x * 32
        self.rect.y = y * 32
        
    def walkto(self, x, y):
        pass