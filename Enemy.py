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
        self.image = pygame.image.load(os.path.join ('Images\Enemies', str(self.type)+'.png'))
        self.rect = self.image.get_rect()

        # Initialize position
        self.setStartPosition(x, y, direction)

    def move(self):
        self.moveThreshold += self.speed / 100.0
        if self.moveThreshold >= 1:
            self.moveThreshold -= 1
            nextX = self.x
            nextY = self.y
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
                    self.y -= 1
                else:
                    self.changeDirection()
            elif self.direction == cardS:
                if (mapY < 0) or ((mapY < mapHeight - 1) and (self.wave.map.M[mapY][mapX] == car_path)):
                    self.y += 1
                else:
                    self.changeDirection()
            elif self.direction == cardW:
                if (mapX > mapWidth - 1) or ((mapX > 0) and (self.wave.map.M[mapY][mapX] == car_path)):
                    self.x -= 1
                else:
                    self.changeDirection()
            elif self.direction == cardE:
                if (mapX < 0) or ((mapX < mapWidth - 1) and (self.wave.map.M[mapY][mapX] == car_path)):
                    self.x += 1
                else:
                    self.changeDirection()

    def changeDirection(self):
        if (self.direction == cardN) or (self.direction == cardS):
            mapX = pixelToMap(self.x)
            mapY = pixelToMap(self.y)
            if (mapX > 0) and (self.wave.map.M[mapY][mapX-1] == car_path):
                self.direction = cardW
                self.x -= 1
                return
            elif (mapX < mapWidth - 2) and (self.wave.map.M[mapY][mapX+1] == car_path):
                self.direction = cardE
                self.x += 1
                return
        elif (self.direction == cardW) or (self.direction == cardE):
            mapX = pixelToMap(self.x)
            mapY = pixelToMap(self.y)
            mapX = pixelToMap(self.x)
            mapY = pixelToMap(self.y)
            if (mapY > 0) and (self.wave.map.M[mapY-1][mapX] == car_path):
                self.direction = cardN
                self.y -= 1
                return
            elif (mapY < mapHeight - 2) and (self.wave.map.M[mapY+1][mapX] == car_path):
                self.direction = cardS
                self.y += 1
                return
        self.kill()
        
    def setStartPosition(self, x, y, direction):
        self.x = x * 32
        self.y = y * 32
        if self.direction == cardN:
            self.y += 32
        elif self.direction == cardS:
            self.y -= 32
        elif self.direction == cardW:
            self.x += 32
        elif self.direction == cardE:
            self.x -= 32
    
    def takeDamage(self, damage):
        damage = max(damage/2, damage-self.armor)
        self.HP = max(0, self.HP - damage)
        if self.HP <= 0:
            self.kill()
    
    def draw(self, screen):
        self.rect.x = self.x
        self.rect.y = self.y
        health_bar_x = self.x
        health_bar_y = self.y + tileSize
        screen.blit(self.image, self.rect)
        screen.fill(red,(health_bar_x, health_bar_y, 32, 4))
        screen.fill(green,(health_bar_x, health_bar_y, (32*self.HP/self.maxHP), 4))