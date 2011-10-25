import pygame, os, Game, Shot
from Global import *
from Util import *
from numpy import *

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
        self.fireThreshold = 0.0
        
        self.image = pygame.image.load(os.path.join ('Images\Towers', str(type+1)+'.png'))
        self.rect = self.image.get_rect()
        self.rect.x = column * tileSize
        self.rect.y = row * tileSize
    
    def basicShoot(self, enemies, screen, shots):
        if self.fireThreshold > 0:
            self.fireThreshold -= 1
        else:
            for enemy in enemies:
                if distPixel(self.rect.y, self.rect.x, enemy.rect.y, enemy.rect.x) <= self.range * tileSize :
                    enemy.damage(self.damage)
                    shots.append(Shot.Shot( \
                        self.rect.x, self.rect.y, enemy.rect.x, enemy.rect.y, \
                        self.type))
                    self.fireThreshold += self.delay
                    return

    def target(self, enemies, screen, shots):
        if self.fireThreshold > 0:
            self.fireThreshold -= 1
        else:
            if self.range == 0:
                # juste splash
                enemy_in_range = 0
                for enemy in enemies:
                    if distPixel(self.rect.x, self.rect.y, \
                        enemy.rect.x, enemy.rect.y) <= self.splash * tileSize:
                        enemy_in_range = 1
                        break
                if enemy_in_range:
                    shots.append(Shot.Shot( \
                        self.rect.x, self.rect.y, enemy.rect.x, enemy.rect.y, \
                        self.type))
                    self.fireThreshold += self.delay
                    for enemy in enemies:
                        if distPixel(self.rect.x, self.rect.y, \
                            enemy.rect.x, enemy.rect.y) <= self.splash * tileSize:
                            enemy.takeDamage(self.damage)
            else:
                if self.splash > 0:
                    # distance, splash
                    extended_range = self.range + self.splash
                    enemy_found = 0
                    for enemy in enemies:
                        if distPixel(self.coords, enemy.coords) <= extended_range:
                            enemy_found = 1
                            break
                    if enemy_found:
                        validPixelList = findValidPixels()
                        max_damage = 0
                        for pixel in validPixelList:
                            # calcule degats totaux
                            pass
                        self.fireThreshold += self.delay
                else:
                    # distance, 1 ennemi
                    max_damage = 0
                    for enemy in enemies:
                        if distPixel(self.rect.x, self.rect.y, \
                            enemy.rect.x, enemy.rect.y) <= self.range * tileSize:
                            potential_damage = min(max(self.damage/2, \
                                self.damage - enemy.armor), enemy.HP)
                            if potential_damage > max_damage:
                                target_enemy = enemy
                                max_damage = potential_damage
                    if max_damage > 0:
                        target_enemy.takeDamage(self.damage)
                        shots.append(Shot.Shot( \
                            self.rect.x, self.rect.y, \
                            target_enemy.rect.x, target_enemy.rect.y, \
                            self.type))
                        self.fireThreshold += self.delay
        
    def fire(self, coords):
        pass
    