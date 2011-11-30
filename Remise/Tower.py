import pygame, os, Game, Shot, Images, Global
from Global import *
from Util import *
from numpy import *
from random import *

class Tower(pygame.sprite.Sprite):
    def __init__(self, row, column, type, level, map):
        pygame.sprite.Sprite.__init__(self)
        self.direction = cardN
        self.drawDirection = cardN
        self.row = row
        self.column = column
        self.firing = 0
        self.justFired = 0
        self.type = type
        self.state = 0
        self.level = level
        self.name = TowerStats[self.type][self.level][TowerNAME]
        self.upgrades = len(TowerStats[self.type]) -1
        self.cooldown = 0
        self.map = map
        self.setParams()
        self.rect = self.image.get_rect()
        self.x = column * tileSize
        self.y = row * tileSize
        self.rect.x = self.x
        self.rect.y = self.y
        self.isMaxLevel = 0

    def drawRadioactivity(self, screen):
        screen.blit(self.radioactivity, (self.x - (self.level*32+96)/2, self.y - (self.level*32+96)/2))

    def draw(self, screen):
        self.rect.x = self.x
        self.rect.y = self.y
        if self.drawDirection != self.direction or self.firing or self.justFired:
            if self.direction == cardN:
                self.image = pygame.transform.rotate(
                    Images.TowerImages[self.type][0+self.firing], 90)
            elif self.direction == cardS:
                self.image = pygame.transform.rotate(
                    Images.TowerImages[self.type][0+self.firing], -90)
            elif self.direction == cardW:
                self.image = pygame.transform.rotate(
                    Images.TowerImages[self.type][0+self.firing], 180)
            elif self.direction == cardE:
                self.image = Images.TowerImages[self.type][0+self.firing]
            elif self.direction == cardNW:
                self.image = pygame.transform.rotate(
                    Images.TowerImages[self.type][2+self.firing], 90)
            elif self.direction == cardNE:
                self.image = Images.TowerImages[self.type][2+self.firing]
            elif self.direction == cardSW:
                self.image = pygame.transform.rotate(
                    Images.TowerImages[self.type][2+self.firing], 180)
            else: # SE
                self.image = pygame.transform.rotate(
                    Images.TowerImages[self.type][2+self.firing], -90)
            if self.justFired:
                self.justFired = 0
            if self.firing:
                self.firing = 0
                self.justFired = 1
            self.drawDirection = self.direction
        screen.blit(self.image, self.rect)

    def update(self, layer):
        pass

    def resetEmplacement(self):
        self.map.S[self.row][self.column] = Images.MapImages[MAPEMPLACEMENT][0]

    def upgrade(self):
        if not self.isMaxLevel:
            Game.placedTower = 1
            self.level += 1
            self.setParams()

    def setParams(self):
        self.value = 0
        for i in range (self.level+1):
            self.value += TowerStats[self.type][i][TowerPRICE]
        if (self.level == self.upgrade) or (self.level == Game.level.levelUpgrades):
            self.isMaxLevel = 1
        else:
            self.isMaxLevel = 0
        self.damage = TowerStats[self.type][self.level][TowerDAMAGE]
        self.delay = TowerStats[self.type][self.level][TowerDELAY]
        self.range = TowerStats[self.type][self.level][TowerRANGE]
        self.splash = TowerStats[self.type][self.level][TowerSPLASH]
        #print self.row, self.column
        self.map.S[self.row][self.column] = Images.MapImages[MAPEMPLACEMENT][self.level]
        self.image = Images.TowerImages[self.type][0]
        if self.type == 5:
            self.radioactivity = pygame.transform.rotate(Images.TowerRadio[self.level], randint(0, 3)*90)
    
    def getFacing(self, target):
        dx, dy = target.x-self.x, target.y-self.y
        if dx > 0:
            if dy > 0:
                if dy*5 < dx*2:
                    self.direction = cardE
                elif dx*5 < dy*2:
                    self.direction = cardS
                else:
                    self.direction = cardSE
            else:
                if -dy*5 < dx*2:
                    self.direction = cardE
                elif dx*5 < -dy*2:
                    self.direction = cardN
                else:
                    self.direction = cardNE
        else:
            if dy > 0:
                if dy*5 < -dx*2:
                    self.direction = cardW
                elif -dx*5 < dy*2:
                    self.direction = cardS
                else:
                    self.direction = cardSW
            else:
                if -dy*5 < -dx*2:
                    self.direction = cardW
                elif -dx*5 < -dy*2:
                    self.direction = cardN
                else:
                    self.direction = cardNW
    
    def target(self, enemies, shots):
        if self.cooldown > 0:
            self.cooldown -= 1
        else:
            ## juste splash
            if self.range == 0:
                # y a-t-il au moins un ennemi a portee?
                enemy_in_range = 0
                for enemy in enemies:
                    if distPixel(self.x, self.y, \
                        enemy.x, enemy.y) <= self.splash:
                        enemy_in_range = 1
                        break
                # si oui, on attaque tous les ennemis a portee
                if enemy_in_range:
                    self.firing = 1
                    self.cooldown += self.delay
                    Global.DataSHOTS += 1
                    #shots.newShot(self.x, self.y, self.x, self.y, self.type, self.level, self.direction)
                    for enemy in enemies:
                        distEnemy = distPixel(self.x, self.y, enemy.x, enemy.y)
                        if distEnemy <= self.splash:
                            damageDealt = int(self.damage[enemy.type] \
                                *(1-1.0*distEnemy/self.splash))
                            Global.DataDAMAGE += min(damageDealt, enemy.HP)
                            enemy.takeDamage(damageDealt)
            else:
                ## distance, splash
                if self.splash > 0:                   
                    # y a-t-il au moins un ennemi a portee?
                    enemy_in_range = 0
                    for enemy in enemies:
                        if distPixel(self.x, self.y, \
                            enemy.x, enemy.y) <= self.range:
                            enemy_in_range = 1
                            break
                    # si oui, on trouve quel ennemi attaquer pour maximiser les degats
                    if enemy_in_range:
                        self.firing = 1
                        self.cooldown += self.delay
                        Global.DataSHOTS += 1
                        hittable_enemies = []
                        splashable_enemies = []
                        for enemy in enemies:
                            if distPixel(self.x, self.y, \
                                enemy.x, enemy.y) <= self.range:
                                hittable_enemies.append(enemy)
                                splashable_enemies.append(enemy)
                            elif distPixel(self.x, self.y, \
                                enemy.x, enemy.y) <= self.range + self.splash:
                                splashable_enemies.append(enemy)
                        max_damage = 0
                        for hit_enemy in hittable_enemies:
                            potential_damage = 0
                            for enemy in splashable_enemies:
                                distEnemy = distPixel(hit_enemy.x, hit_enemy.y, \
                                    enemy.x, enemy.y)
                                if distEnemy <= self.splash:
                                    potential_damage += enemy.value * \
                                        min(int(self.damage[enemy.type] \
                                            *(1-1.0*distEnemy/self.splash)), \
                                            enemy.HP)
                            if potential_damage > max_damage:
                                target_enemy = hit_enemy
                                max_damage = potential_damage
                        for enemy in splashable_enemies:
                            distEnemy = distPixel(target_enemy.x, target_enemy.y, \
                                enemy.x, enemy.y)
                            if distEnemy <= self.splash:
                                damageDealt = int(self.damage[enemy.type] \
                                    *(1-1.0*distEnemy/self.splash))
                                Global.DataDAMAGE += min(damageDealt, enemy.HP)
                                enemy.takeDamage(damageDealt)
                        self.getFacing(target_enemy)
                        shots.newShot(self.x, self.y, target_enemy.x, target_enemy.y, self.type, self.level, self.direction)
                ## distance, 1 ennemi
                else:
                    # a quel ennemi causerait-on le plus de dommages?
                    max_damage = 0
                    for enemy in enemies:
                        if distPixel(self.x, self.y, \
                            enemy.x, enemy.y) <= self.range:
                            if self.delay <= 32:
                                potential_damage = enemy.value * \
                                    self.damage[enemy.type]
                            else:
                                potential_damage = enemy.value * \
                                    min(self.damage[enemy.type], enemy.HP)
                            if potential_damage > max_damage:
                                target_enemy = enemy
                                max_damage = potential_damage
                    # si on en a trouve un, on l'attaque
                    if max_damage > 0:
                        self.firing = 1
                        self.cooldown += self.delay
                        Global.DataSHOTS += 1
                        enemy = target_enemy
                        damageDealt = self.damage[enemy.type]
                        Global.DataDAMAGE += min(damageDealt, enemy.HP)
                        enemy.takeDamage(damageDealt)
                        self.getFacing(target_enemy)
                        shots.newShot(self.x, self.y, target_enemy.x, target_enemy.y, self.type, self.level, self.direction)
                        