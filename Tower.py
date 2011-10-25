import pygame, os, Game, Shot
from Global import *
from Util import *

class Tower(pygame.sprite.Sprite):
    def __init__(self, row, column, type):
        pygame.sprite.Sprite.__init__(self)

        self.type = type
        self.name = TowerTypes[self.type][TowerNAME]
        self.value = TowerTypes[self.type][TowerVALUE]
        self.damage = TowerTypes[self.type][TowerDAMAGE]
        self.delay = TowerTypes[self.type][TowerDELAY]
        self.range = TowerTypes[self.type][TowerRANGE]
        self.splash = TowerTypes[self.type][TowerSPLASH]
        
        self.image = pygame.image.load(os.path.join ('Images\Towers', str(type+1)+'.png'))
        self.rect = self.image.get_rect()
        self.rect.x = column * tileSize
        self.rect.y = row * tileSize
    
    def basicShoot(self, enemies, screen, shots):
        for enemy in enemies:
            if distPixel(self.rect.y, self.rect.x, enemy.rect.y, enemy.rect.x) <= self.range * tileSize :
                enemy.damage(self.damage)
                shots.append(Shot.Shot( \
                    self.rect.x, self.rect.y, enemy.rect.x, enemy.rect.y, \
                    self.type))
                return

    def target(self, enemies, screen, shots):
        if self.range == 0:
            # juste splash
            enemy_in_range = 0
            for enemy in enemies:
                if dist_pixel(self.coords, enemy.coords) <= self.range:
                    enemy_in_range = 1
                    enemy.damage(self.damage)
            if enemy_in_range = 1:
                shots.append(Shot.Shot( \
                    self.rect.x, self.rect.y, enemy.rect.x, enemy.rect.y, \
                    self.type))
        else:
            if self.splash > 0:
                # distance, splash
                extended_range = self.range + self.splash
                enemy_found = 0
                for enemy in enemies:
                    if dist_pixel(self.coords, enemy.coords) <= extended_range:
                        enemy_found = 1
                        break
                if enemy_found:
                    validPixelList = findValidPixels()
                    max_damage = 0
                    for pixel in validPixelList:
                        # calcule degats totaux
                        pass
            else:
                # distance, 1 ennemi
                validEnemyList = []
                for enemy in enemies:
                    if dist_pixel(self.coords, enemy.coords) <= self.range:
                        validEnemyList.append(enemy)
                max_damage = 0
                for enemy in validEnemyList:
                    damage_done = 
                    if damage_done > max_damage:
                        chosen_enemy = enemy
                        max_damage = damage_done
                     

    def fire(self, coords):
        pass
    