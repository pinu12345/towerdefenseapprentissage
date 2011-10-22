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
        if self.range == 0:
            # juste splash
            for enemy in enemyList:
                if dist_pixel(self.coords, enemy.coords) <= self.range:
                    self.fire(self.coords)
                    return None
        else:
            if self.splash > 0:
                # distance, splash
                extended_range = self.range + self.splash
                enemy_found = 0
                for enemy in enemyList:
                    if dist_pixel(self.coords, enemy.coords) <= extended_range:
                        enemy_found = 1
                        break
                if enemy_found:
                    validPixelList = findValidPixels()
                    max_damage = 0
                    for pixel in validPixelList:
                        # calcule dégâts totaux
                        pass
            else:
                # distance, 1 ennemi
                validEnemyList = []
                for enemy in enemyList:
                    if dist_pixel(self.coords, enemy.coords) <= self.range:
                        validEnemyList.append(enemy)
                max_damage = 0
                for enemy in validEnemyList:
                    pass
                