import sys, os, pygame, Game, Images
from Global import *

class Menu():
    def __init__(self, map, wave, towers):
        self.redraw = 0
        self.btnPause = BtnPause(875,300)
        self.btnMenu = BtnMenu(775,350)
        self.btnLowerSpeed = BtnLowerSpeed(875,350)
        self.btnIncreaseSpeed = BtnIncreaseSpeed(775,400)
        self.map = map
        self.wave = wave
        self.towers = towers
        self.menu = pygame.sprite.Group()
        #self.menu.add(self.btnStart, self.btnRandom, self.btnBack, self.btnExit, self.btnRandomSpawn)
        #self.menu.add(self.btnDino1, self.btnDino10, self.btnDinoJr2, self.btnDinoJr20, self.btnNinja5, self.btnNinja50, self.btnPirate5, self.btnPirate50, self.btnSinge10, self.btnSinge100)

    def draw(self, screen):
        ##Next Wave : 790, 460
        currentWave = Game.level.currentWave
        maxWave = Game.level.maxWave - 1
        screen.blit(Images.InterfaceBGopaque, (790, 460) , (790, 460, tileSize, tileSize), 0)
        screen.blit(Images.EnemyImages[Game.level.levelWaves[currentWave][0]], (790, 460), (0, 0, tileSize, tileSize), 0)
        
        #Redraw the background
        for i in range(0, 5):
            screen.blit(Images.InterfaceBGwashed, (784, 370 - i*56) , (784, 370 - i*56, 194, 44), 0)

        #Draw the next waves
        for i in range(0, maxWave - currentWave):
            if i <= 4:
                screen.blit(Images.InterfaceBGopaque, (784, 370 - i*56) , (784, 370 - i*56, 194, 44), 0)
                screen.blit(Images.EnemyImages[Game.level.levelWaves[currentWave + i + 1][0]], (790, 376 - i*56), (0, 0, tileSize, tileSize), 0)

        print Game.level.levelWaves[currentWave][0]
        self.redraw = 0

    def onClick(self, pos, map):
        if self.btnPause.rect.collidepoint(pos):
            Game.state = STATE_GAME
        elif self.btnMenu.rect.collidepoint(pos):
            self.wave.clear()
            self.towers.clear()
            map.loadRandomMap()
            self.wave.newRandomSpawn()
            Game.state = STATE_LOADGAME
        elif self.btnLowerSpeed.rect.collidepoint(pos):
            Game.state = STATE_INITGAMEMENU
        elif self.btnIncreaseSpeed.rect.collidepoint(pos):
            self.wave.clear()
            self.wave.newSpawn(4, 1)

class BtnPause(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join ('Images\Buttons', 'ok.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class BtnMenu(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join ('Images\Buttons', 'A.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
 
class BtnLowerSpeed(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join ('Images\Buttons', 'B.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
 
class BtnIncreaseSpeed(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join ('Images\Buttons', 'Dino1.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y