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

    def showTower(self, screen, tower, level = 0):
        screen.blit(Images.InterfaceBGopaque, (196, 512) , (196, 512, 796, 116), 0)
        x = 206
        y = 524
        screen.blit(pygame.transform.scale2x(Images.TowerImages[tower][0]), (x, y), None, 0)
        screen.blit(Images.InterfaceLevels[level], (x + 48, y + 68), None, 0)
        for i in range(len(Images.EnemyImages)):
            size = TowerStats[tower][level][11][i]
            screen.fill(barColor, (654 + i*36, 574 - size, 28, size), 0)
            screen.blit(Images.EnemyImages[i], (652 + i*36, 576), (0, 0, tileSize, tileSize), 0)
        for j in range(4):
            size = TowerStats[tower][level][7+j]
            screen.fill(barColor, (478 + j*40, 574 - size, 28, size), 0)

    def draw(self, screen):
        ##Next Wave : 790, 460
        currentWave = Game.level.currentWave
        maxWave = Game.level.maxWave - 1

        #Redraw the background
        for i in range(0, 5):
            screen.blit(Images.InterfaceBGwashed, (784, 370 - i*56) , (784, 370 - i*56, 194, 44), 0)
        if currentWave > maxWave:
            screen.blit(Images.InterfaceBGwashed, (784, 454) , (784, 454, 194, 44), 0)
        else:
            #Draw the next waves
            screen.blit(Images.InterfaceBGopaque, (784, 454) , (784, 454, 194, 44), 0)
            screen.blit(Images.EnemyImages[Game.level.levelWaves[currentWave][0]], (790, 460), (0, 0, tileSize, tileSize), 0)
            for j in range(3):
                size = EnemyStats[Game.level.levelWaves[currentWave][0]][7+j]
                screen.fill(barColor, (916 + j*20, 478 - size, 16, size), 0)
            for i in range(0, maxWave - currentWave):
                if i <= 4:
                    enemyType = Game.level.levelWaves[currentWave + i + 1][0]
                    screen.blit(Images.InterfaceBGopaque, (784, 370 - i*56) , (784, 370 - i*56, 194, 44), 0)
                    screen.blit(Images.EnemyImages[enemyType], (790, 376 - i*56), (0, 0, tileSize, tileSize), 0)
                    ##BLIT LA PETITE IMAGE
                    for j in range(3):
                        size = EnemyStats[enemyType][7+j]
                        screen.fill(barColor, (916 + j*20, 394 - i*56 - size, 16, size), 0)
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