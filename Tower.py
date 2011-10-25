import pygame, os, Game
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
    
    def basicShoot(self, enemies, screen):
        for enemy in enemies:
            if distPixel(self.rect.y, self.rect.x, enemy.rect.y, enemy.rect.x) <= self.range * tileSize :
                enemy.damage(self.damage)
                pygame.draw.aaline(screen, (255, 255, 220), (self.rect.x + tileSize/2, self.rect.y + tileSize/2), (enemy.rect.x + tileSize/2, enemy.rect.y + tileSize/2), 1)
                return

    def target(self, enemies):
        if self.range == 0:
            # juste splash
            for enemy in enemies:
                if dist_pixel(self.coords, enemy.coords) <= self.range:
                    self.fire(self.coords)
                    return None
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
                    pass

    def fire(self, coords):
        pass
    