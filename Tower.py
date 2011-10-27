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
        self.range = TowerTypes[self.type][TowerRANGE] * tileSize
        self.splash = TowerTypes[self.type][TowerSPLASH] *tileSize
        self.cooldown = 0.0
        
        self.image = pygame.image.load(os.path.join ('Images\Towers', str(type+1)+'.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.x = column * tileSize
        self.rect.y = row * tileSize

    def target(self, enemies, screen, shots):
        # est-ce que le cooldown est ecoule?
        if self.cooldown > 0:
            self.cooldown -= 1
        else:
            
            ## juste splash
            if self.range == 0:
                # y a-t-il au moins un ennemi a portee?
                enemy_in_range = 0
                for enemy in enemies:
                    if distPixel(self.rect.x, self.rect.y, \
                        enemy.rect.x, enemy.rect.y) <= self.splash:
                        enemy_in_range = 1
                        break
                # si oui, on attaque tous les ennemis a portee
                if enemy_in_range:
                    shots.append(Shot.Shot( \
                        self.rect.x, self.rect.y, self.rect.x, self.rect.y, \
                        self.type))
                    for enemy in enemies:
                        if distPixel(self.rect.x, self.rect.y, \
                            enemy.rect.x, enemy.rect.y) <= self.splash:
                            enemy.takeDamage(self.damage)
                    self.cooldown += self.delay
            else:
                
                ## distance, splash
                if self.splash > 0:
                    # y a-t-il au moins un ennemi a portee?
                    extended_range = self.range + self.splash
                    enemy_in_range = 0
                    for enemy in enemies:
                        if distPixel(self.rect.x, self.rect.y, \
                            enemy.rect.x, enemy.rect.y) <= extended_range:
                            enemy_in_range = 1
                            break
                    # si oui, on trouve quel pixel attaquer pour maximiser les dommages
                    if enemy_in_range:
                        validPixels = self.findValidPixels()
                        max_damage = 0
                        max_distance = 0
                        #####
                        # print "\n Evaluating valid pixels..."
                        validPixels_num = 0
                        #####
                        for pixel in validPixels:
                            #####
                            validPixels_num += 1
                            #####
                            potential_damage = 0
                            for enemy in enemies:
                                if distPixel(pixel[0], pixel[1], \
                                    enemy.rect.x, enemy.rect.y) <= self.splash:
                                    potential_damage += min(max(self.damage/2, \
                                        self.damage - enemy.armor), enemy.HP)
                            if potential_damage > max_damage:
                                target_pixel = pixel
                                max_damage = potential_damage
                                max_distance = distPixel(pixel[0], pixel[1], \
                                    self.rect.x, self.rect.y)
                            elif potential_damage == max_damage and \
                                distPixel(pixel[0], pixel[1], \
                                self.rect.x, self.rect.y) < max_distance:
                                target_pixel = pixel
                                max_distance = distPixel(pixel[0], pixel[1], \
                                    self.rect.x, self.rect.y)
                        # on attaque le pixel trouve
                        #####
                        # print " Verified", validPixels_num, "pixels."
                        #####
                        shots.append(Shot.Shot(self.rect.x, self.rect.y, \
                            target_pixel[0], target_pixel[1], self.type))
                        for enemy in enemies:
                            if distPixel(target_pixel[0], target_pixel[1], \
                                enemy.rect.x, enemy.rect.y) <= self.splash:
                                enemy.takeDamage(self.damage)
                        self.cooldown += self.delay
                
                ## distance, 1 ennemi
                else:
                    # a quel ennemi causerait-on le plus de dommages?
                    max_damage = 0
                    for enemy in enemies:
                        if distPixel(self.rect.x, self.rect.y, \
                            enemy.rect.x, enemy.rect.y) <= self.range:
                            potential_damage = min(max(self.damage/2, \
                                self.damage - enemy.armor), enemy.HP)
                            if potential_damage > max_damage:
                                target_enemy = enemy
                                max_damage = potential_damage
                    # si on en a trouve un, on l'attaque
                    if max_damage > 0:
                        target_enemy.takeDamage(self.damage)
                        shots.append(Shot.Shot( \
                            self.rect.x, self.rect.y, \
                            target_enemy.rect.x, target_enemy.rect.y, \
                            self.type))
                        self.cooldown += self.delay
        
    def findValidPixels(self):
        #####
        # print "\n Finding valid pixels..."
        validPixels_num = 0
        #####
        validPixels = []
        imin = min(0, self.rect.x-self.range)
        imax = max(self.rect.x+self.range+1, mapWidth*tileSize+1)
        jmin = min(0, self.rect.y-self.range)
        jmax = max(self.rect.y+self.range+1, mapHeight*tileSize+1)
        pixelStep = tileSize
        for i in range(imin, imax, pixelStep):
            for j in range(jmin, jmax, pixelStep):
                if distPixel(self.rect.x, self.rect.y, i, j) < self.range:
                    validPixels.append([i, j])
                    #####
                    validPixels_num += 1
        # print " Returning", validPixels_num, "pixels."
        #####
        return validPixels
        
    def fire(self, coords):
        pass
    