import pygame, os

NAME = 0
VALUE = 1
DAMAGE = 2
DELAY = 3
RANGE = 4
SPLASH = 5

## Tower Types
## Nom              Value   Damage  Delay   Range   Splash
Types = \
    [["Mitraille",  100,    2,      0.1,    4,      0],
    ["Sniper",      200,    200,    4,      10,     0],
    ["Zone",        100,    20,     1,      0,      2],
    ["Omega",       500,    200,    2,      12,     1],
    ["Hax",         1,      1000,   0.1,    100,    5]]

class Tower(pygame.sprite.Sprite):
    def __init__(self, xy, type):
        pygame.sprite.Sprite.__init__(self)
        
        self.name = Types[self.type][NAME]
        self.value = Types[self.type][VALUE]
        self.damage = Types[self.type][DAMAGE]
        self.delay = Types[self.type][DELAY]
        self.range = Types[self.type][RANGE]
        self.splash = Types[self.type][SPLASH]
        
        towerList.append(self)

        x, y = xy
        self.level = 1

        self.imgList = None
        self.loadImages()

        self.type = type
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.surfx, self.surfy = self.rect.center
        self.surfx -= 100
        self.surfy -= 100

    def target(self):
        for enemy in baddieList:
            aimx = enemy.rect.centerx
            aimy = enemy.rect.bottom - 13
            if self.range == 0:
                enemy.health -= self.damage
                return (aimx,aimy)
            elif dist((aimx,aimy),self.rect,self.range) == 1:
                enemy.health -= self.damage
                return (aimx,aimy)