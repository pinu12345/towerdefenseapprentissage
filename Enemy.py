import pygame, os, random
from Game import *
from Global import *
from Util import *
from Images import *

type = 0

# Colors
red    = ( 255,  40,  20)
green  = (   0, 255,  20)

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
        valid_cars = [car_path, car_base]
        mapX = min(pixelToMap(self.x), mapWidth-1)
        mapY = min(pixelToMap(self.y), mapHeight-1)
        if self.direction in [cardN, cardS]:
            if (mapX > 0) and self.wave.map.M[mapY][mapX-1] in valid_cars:
                self.direction = cardW
                self.x -= 1
                return
            elif (mapX < mapWidth - 2) and self.wave.map.M[mapY][mapX+1] in valid_cars:
                self.direction = cardE
                self.x += 1
                return
        elif self.direction in [cardW, cardE]:
            if (mapY > 0) and self.wave.map.M[mapY-1][mapX] in valid_cars:
                self.direction = cardN
                self.y -= 1
                return
            elif (mapY < mapHeight - 2) and self.wave.map.M[mapY+1][mapX] in valid_cars:
                self.direction = cardS
                self.y += 1
                return
        ## Fin de la partie
        if Game.state != STATE_PREPARATION:
            if Game.state != STATE_ENDWAVE:
                print '\n An enemy got through!'
            Game.state = STATE_ENDWAVE
            Game.restartWave = 1
            Game.redrawSPBtn = 1
            self.wave.clear()
            #Game.level.restart()
            #Game.level.logWave(0)
            #if Game.balanceMode:
                #Game.level.balanceWave()
            #else:
                #Game.level.autoWave()
                
        
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
            ## Verifie s'il reste encore des ennemis
            self.kill()
            Game.enemyCount -= 1
            if Game.enemyCount == 0:
                #print ' Wave completed'
                Game.state = STATE_ENDWAVE
                Game.redrawSPBtn = 1
                Game.nextWave = 1

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