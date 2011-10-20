import pygame, os, random
from Game import *

type = 0

NAME = 0
VALUE = 1
HP = 2
ARMOR = 3
SPEED = 4
DELAY = 5

## Enemy Types
## Nom              Valeur  HP      Armor   Speed   Delay
Types = \
    [["Ninja",      5,      100,    0,      8,      1],
    ["Pirate",      5,      200,    0,      2,      1],
    ["Singe",       1,      50,     0,      100,    0.25],
    ["BebeDino",    1,      200,    5,      2,      2],
    ["Dinosaure",   40,     1000,   10,     1,      4]]

class Enemy(pygame.sprite.Sprite):
    def __init__(self, type, wave, x, y):
        
        # Set the enemy type
        self.type = type
        self.wave = wave

        # Set the enemy parameters
        self.name = Type[self.type][NAME]
        self.value = Type[self.type][VALUE]
        self.hp = Types[self.type][HP]
        self.armor = Type[self.type][ARMOR]
        self.speed = Types[self.type][SPEED]
        
        # Required by Sprite
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join ('Images\Enemies', str(self.type)+'.png'))
        self.rect = self.image.get_rect()

        # Initialize position
        self.setPosition(x, y)

    def move(self, direction):
        if self.rect.x > 500:
            self.rect.x = 0
        self.rect.x += varX * self.speed

    def update(self):
        pass
        
    def setPosition(self, x, y):
        self.rect.x = self.wave.tileSize * x + 1
        self.rect.y = self.wave.tileSize * y + 1
        
    def walkto(self, x, y):
        pass
