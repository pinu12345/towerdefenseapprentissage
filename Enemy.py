import pygame, os, random
from Game import *
from Global import *
from Util import *
from Images import *

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
        self.drawDirection = cardE

        # Set the enemy parameters
        self.name = EnemyStats[self.type][EnemyNAME]
        self.value = EnemyStats[self.type][EnemyVALUE]
        self.maxHP = 10000
        self.HP = self.maxHP
        self.speed = EnemyStats[self.type][EnemySPEED]
        self.spread = EnemyStats[self.type][EnemySPREAD]
        self.dim = EnemyStats[self.type][EnemyDIM]
        self.HPbar = EnemyStats[self.type][EnemyHPBAR]
        
        # Required by Sprite
        pygame.sprite.Sprite.__init__(self)
        self.image = Images.EnemyImages[self.type]
        self.rect = self.image.get_rect()

        # Initialize position
        self.setStartPosition(x, y, direction)

    def move(self):
        pixelsToGo = self.speed
        while pixelsToGo > 0:
            pixelsToGo -= 1
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
                if (mapY > mapHeight - 1) or ((mapY > 0) and ((self.wave.map.M[mapY][mapX] == car_path) or (self.wave.map.M[mapY][mapX] == car_base))):
                    self.y -= 1
                else:
                    self.changeDirection()
            elif self.direction == cardS:
                if (mapY < 0) or ((mapY < mapHeight - 1) and ((self.wave.map.M[mapY][mapX] == car_path) or (self.wave.map.M[mapY][mapX] == car_base))):
                    self.y += 1
                else:
                    self.changeDirection()
            elif self.direction == cardW:
                if (mapX > mapWidth - 1) or ((mapX > 0) and ((self.wave.map.M[mapY][mapX] == car_path) or (self.wave.map.M[mapY][mapX] == car_base))):
                    self.x -= 1
                else:
                    self.changeDirection()
            elif self.direction == cardE:
                if (mapX < 0) or ((mapX < mapWidth - 1) and ((self.wave.map.M[mapY][mapX] == car_path) or (self.wave.map.M[mapY][mapX] == car_base))):
                    self.x += 1
                else:
                    self.changeDirection()

    def changeDirection(self):
        if (self.direction == cardN) or (self.direction == cardS):
            mapX = pixelToMap(self.x)
            mapY = pixelToMap(self.y)
            if (mapX > 0) and ((self.wave.map.M[mapY][mapX-1] == car_path) or (self.wave.map.M[mapY][mapX-1] == car_base)):
                self.direction = cardW
                self.x -= 1
                return
            elif (mapX < mapWidth - 2) and ((self.wave.map.M[mapY][mapX+1] == car_path) or (self.wave.map.M[mapY][mapX+1] == car_base)):
                self.direction = cardE
                self.x += 1
                return
        elif (self.direction == cardW) or (self.direction == cardE):
            mapX = pixelToMap(self.x)
            mapY = pixelToMap(self.y)
            mapX = pixelToMap(self.x)
            mapY = pixelToMap(self.y)
            if (mapY > 0) and ((self.wave.map.M[mapY-1][mapX] == car_path) or (self.wave.map.M[mapY-1][mapX] == car_base)):
                self.direction = cardN
                self.y -= 1
                return
            elif (mapY < mapHeight - 2) and ((self.wave.map.M[mapY+1][mapX] == car_path) or (self.wave.map.M[mapY+1][mapX] == car_base)):
                self.direction = cardS
                self.y += 1
                return
        ## Fin de la partie
        if Game.state != STATE_PREPARATION:
            Game.state = STATE_PREPARATION
            self.wave.clear()
            
            #print 'An enemy has passed, restarting level...'
            #Game.level.restart()
            
            print 'An enemy has passed, restarting wave...'
            Game.level.restartWave()
        
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
        self.HP = max(0, self.HP - damage)
        if self.HP <= 0:
            ## Verifie si il reste encore des enemies
            self.kill()
            Game.enemyCount -= 1
            if Game.enemyCount == 0:
                print 'Wave completed'
                Game.state = STATE_PREPARATION
                Game.level.nextWave()
    
    def draw(self, screen):
        if self.drawDirection != self.direction:
            if self.drawDirection == cardN:
                if self.direction == cardW:
                    self.image = pygame.transform.rotate(self.image, 90)
                elif self.direction == cardS:
                    self.image = pygame.transform.rotate(self.image, 180)
                elif self.direction == cardE:
                    self.image = pygame.transform.rotate(self.image, 270)
            elif self.drawDirection == cardS:
                if self.direction == cardW:
                    self.image = pygame.transform.rotate(self.image, 270)
                elif self.direction == cardN:
                    self.image = pygame.transform.rotate(self.image, 180)
                elif self.direction == cardE:
                    self.image = pygame.transform.rotate(self.image, 90)
            elif self.drawDirection == cardE:
                if self.direction == cardS:
                    self.image = pygame.transform.rotate(self.image, 270)
                elif self.direction == cardW:
                    self.image = pygame.transform.rotate(self.image, 180)
                elif self.direction == cardN:
                    self.image = pygame.transform.rotate(self.image, 90)
            elif self.drawDirection == cardW:
                if self.direction == cardS:
                    self.image = pygame.transform.rotate(self.image, 90)
                elif self.direction == cardE:
                    self.image = pygame.transform.rotate(self.image, 180)
                elif self.direction == cardN:
                    self.image = pygame.transform.rotate(self.image, 270)
            self.drawDirection = self.direction
        self.rect.x = self.x
        self.rect.y = self.y
        health_bar_width = self.HPbar
        health_bar_x = self.x + (32-health_bar_width)/2
        health_bar_y = self.y + tileSize + 2 + self.dim//10 - (32-self.dim)/2
        screen.blit(self.image, self.rect)
        screen.fill(red, (health_bar_x, health_bar_y, health_bar_width, 4))
        screen.fill(green, (health_bar_x, health_bar_y, \
            (health_bar_width * self.HP/self.maxHP), 4))
    
    def update(self, screen):
        pass