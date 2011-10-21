import pygame, os
from Global import *

class Tower(pygame.sprite.Sprite):
    def __init__(self, xy, type):
        pygame.sprite.Sprite.__init__(self)
        
        self.name = TowerTypes[self.type][TowerNAME]
        self.value = TowerTypes[self.type][TowerVALUE]
        self.damage = TowerTypes[self.type][TowerDAMAGE]
        self.delay = TowerTypes[self.type][TowerDELAY]
        self.range = TowerTypes[self.type][TowerRANGE]
        self.splash = TowerTypes[self.type][TowerSPLASH]
        
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