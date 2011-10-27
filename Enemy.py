import pygame, os, random
from Game import *
from Global import *
from Util import *

type = 0

# Colors
red    = ( 255,  20,  20)
green  = (   0, 255,   0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, type, wave, x, y, direction, id):
        
        self.id = id
        # Set the enemy type
        self.type = type
        self.wave = wave
        self.direction = direction
        self.moveThreshold = 0.0

        # Set the enemy parameters
        self.name = EnemyTypes[self.type][EnemyNAME]
        self.value = EnemyTypes[self.type][EnemyVALUE]
        self.maxHP = EnemyTypes[self.type][EnemyHP]
        self.HP = self.maxHP
        self.armor = EnemyTypes[self.type][EnemyARMOR]
        self.speed = EnemyTypes[self.type][EnemySPEED]
        
        # Required by Sprite
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join ('Images\Enemies', str(self.type)+'.png')).convert()
        self.rect = self.image.get_rect()

        # Initialize position
        self.setStartPosition(x, y, direction)
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        # Health bar
        health_bar_x = self.rect.x
        health_bar_y = self.rect.y + tileSize
        screen.fill(red,(health_bar_x, health_bar_y, 32, 4))
        screen.fill(green,(health_bar_x, health_bar_y, (32*self.HP/self.maxHP), 4))
    
    def move(self):
        self.moveThreshold += self.speed / 100.0
        if self.moveThreshold >= 1:
            self.moveThreshold -= 1
            nextX = self.rect.x
            nextY = self.rect.y
            if self.direction == cardN:
                nextY -= 1
            elif self.direction == cardS:
                nextY += 32
            elif self.direction == cardW:
                nextX -= 1
            elif self.direction == cardE:
                nextX += 32
            mapY = pixelToMap(nextY)
            mapX = pixelToMap(nextX)

            if self.direction == cardN:
                if (mapY > mapHeight - 1) or ((mapY > 0) and (self.wave.map.M[mapY][mapX] == car_path)):
                    self.rect.y -= 1
                else:
                    self.changeDirection()
            elif self.direction == cardS:
                if (mapY < 0) or ((mapY < mapHeight - 1) and (self.wave.map.M[mapY][mapX] == car_path)):
                    self.rect.y += 1
                else:
                    self.changeDirection()
            elif self.direction == cardW:
                if (mapX > mapWidth - 1) or ((mapX > 0) and (self.wave.map.M[mapY][mapX] == car_path)):
                    self.rect.x -= 1
                else:
                    self.changeDirection()
            elif self.direction == cardE:
                if (mapX < 0) or ((mapX < mapWidth - 1) and (self.wave.map.M[mapY][mapX] == car_path)):
                    self.rect.x += 1
                else:
                    self.changeDirection()

    def changeDirection(self):
        if (self.direction == cardN) or (self.direction == cardS):
            mapX = pixelToMap(self.rect.x)
            mapY = pixelToMap(self.rect.y)
            if (mapX > 0) and (self.wave.map.M[mapY][mapX-1] == car_path):
                self.direction = cardW
                self.rect.x -= 1
                return
            elif (mapX < mapWidth - 2) and (self.wave.map.M[mapY][mapX+1] == car_path):
                self.direction = cardE
                self.rect.x += 1
                return
        elif (self.direction == cardW) or (self.direction == cardE):
            mapX = pixelToMap(self.rect.x)
            mapY = pixelToMap(self.rect.y)
            mapX = pixelToMap(self.rect.x)
            mapY = pixelToMap(self.rect.y)
            if (mapY > 0) and (self.wave.map.M[mapY-1][mapX] == car_path):
                self.direction = cardN
                self.rect.y -= 1
                return
            elif (mapY < mapHeight - 2) and (self.wave.map.M[mapY+1][mapX] == car_path):
                self.direction = cardS
                self.rect.y += 1
                return
        self.kill()
        
    def setStartPosition(self, x, y, direction):
        self.rect.x = x * 32
        self.rect.y = y * 32
        if self.direction == cardN:
            self.rect.y += 32
        elif self.direction == cardS:
            self.rect.y -= 32
        elif self.direction == cardW:
            self.rect.x += 32
        elif self.direction == cardE:
            self.rect.x -= 32
    
    def takeDamage(self, damage):
        damage = max(damage/2, damage-self.armor)
        self.HP = max(0, self.HP - damage)
        if self.HP <= 0:
            self.kill()
