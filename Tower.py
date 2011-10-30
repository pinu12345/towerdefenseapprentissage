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
        
        self.image = pygame.image.load(os.path.join ('Images\Towers', str(type+1)+'.png'))
        self.rect = self.image.get_rect()
        self.x = column * tileSize
        self.y = row * tileSize
        self.rect.x = self.x
        self.rect.y = self.y

    def target(self, enemies, shots):
        # est-ce que le cooldown est ecoule?
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
                    shots.newShot(self.x, self.y, self.x, self.y, self.type)
                    for enemy in enemies:
                        if distPixel(self.x, self.y, \
                            enemy.x, enemy.y) <= self.splash:
                            enemy.takeDamage(self.damage)
                    self.cooldown += self.delay
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
                    # si oui, on trouve quel ennemi attaquer pour maximiser les dommages
                    if enemy_in_range:
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
                        for enemy in hittable_enemies:
                            potential_damage = 0
                            for other_enemy in splashable_enemies:
                                if distPixel(enemy.x, enemy.y, \
                                    other_enemy.x, other_enemy.y) \
                                    <= self.splash:
                                    potential_damage += min(max(self.damage/2, \
                                        self.damage - other_enemy.armor), \
                                        other_enemy.HP)
                            if potential_damage > max_damage:
                                target_enemy = enemy
                                max_damage = potential_damage
                        shots.newShot(self.x, self.y, target_enemy.x, target_enemy.y, self.type)
                        for other_enemy in splashable_enemies:
                            if distPixel(target_enemy.x, target_enemy.y, \
                                other_enemy.x, other_enemy.y) \
                                <= self.splash:
                                other_enemy.takeDamage(self.damage)
                        self.cooldown += self.delay
                
                ## distance, 1 ennemi
                else:
                    # a quel ennemi causerait-on le plus de dommages?
                    max_damage = 0
                    for enemy in enemies:
                        if distPixel(self.x, self.y, \
                            enemy.x, enemy.y) <= self.range:
                            potential_damage = min(max(self.damage/2, \
                                self.damage - enemy.armor), enemy.HP)
                            if potential_damage > max_damage:
                                target_enemy = enemy
                                max_damage = potential_damage
                    # si on en a trouve un, on l'attaque
                    if max_damage > 0:
                        target_enemy.takeDamage(self.damage)
                        shots.newShot(self.x, self.y, target_enemy.x, target_enemy.y, self.type)
                        self.cooldown += self.delay
        