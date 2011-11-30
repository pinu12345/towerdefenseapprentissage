import sys, os, pygame, Game, Images
from Global import *

class Menu():
    def __init__(self, map, wave, towers):
        self.redraw = 0
        self.redrawSpeed = 0
        Game.redrawSPBtn = 0
        self.drawSpeed = 1
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

    def drawSpeedArrows(self, screen):
        screen.blit(Images.InterfaceBGwashed, (850, 62) , (850, 62, 62, 24), 0)
        for i in range (self.drawSpeed):
            screen.blit(Images.InterfaceBGopaque, (850 + i*16, 62) , (850 + i*16, 62, 16, 24), 0)
        self.redrawSpeed = 0

    def drawSPBtn(self, screen):
        if Game.redrawSPBtn == 1:
            screen.blit(Images.InterfaceStart, (784, 14) , None, 0)
        elif Game.redrawSPBtn == 2:
            screen.blit(Images.InterfacePause, (784, 14) , None, 0)
        Game.redrawSPBtn = 0

    def draw(self, screen):
        ##Next Wave : 790, 460
        currentWave = Game.level.currentWave
        maxWave = Game.level.maxWave - 1
        
        
        #Redraw the background
        screen.blit(Images.InterfaceBGwashed, (768, 0), (768, 0, 224, 514))
        
        for i in range(0, 5):
            screen.blit(Images.InterfaceBGwashed, (784, 370 - i*56) , (784, 370 - i*56, 194, 44), 0)
        if currentWave > maxWave:
            screen.blit(Images.InterfaceBGwashed, (784, 454) , (784, 454, 194, 44), 0)
        else:
            #Draw the next waves
            screen.blit(Images.InterfaceBGopaque, (784, 454) , (784, 454, 194, 44), 0)
            screen.blit(Images.EnemyImages[Game.level.levelWaves[currentWave][0]], (790, 460), None, 0)
            screen.blit(Images.InterfaceType[EnemyStats[Game.level.levelWaves[currentWave][0]][6]], (918, 480), None, 0)
            screen.blit(Game.enemyCountFont.render('x ' + str(Game.level.levelWaves[currentWave][1]), 0, (0, 128, 153)), (835, 464), None, 0)
            for j in range(3):
                size = EnemyStats[Game.level.levelWaves[currentWave][0]][7+j]
                screen.fill(barColor, (916 + j*20, 478 - size, 16, size), 0)
            for i in range(0, maxWave - currentWave):
                if i <= 4:
                    enemyType = Game.level.levelWaves[currentWave + i + 1][0]
                    enemyCount = 'x ' + str(Game.level.levelWaves[currentWave + i + 1][1])
                    screen.blit(Images.InterfaceBGopaque, (784, 370 - i*56) , (784, 370 - i*56, 194, 44), 0)
                    screen.blit(Images.EnemyImages[enemyType], (790, 376 - i*56), None, 0)
                    screen.blit(Images.InterfaceType[EnemyStats[enemyType][6]], (918, 396 - i*56), None, 0)
                    screen.blit(Game.enemyCountFont.render(enemyCount, 0, (0, 128, 153)), (835, 380 - i*56), None, 0)
                    for j in range(3):
                        size = EnemyStats[enemyType][7+j]
                        screen.fill(barColor, (916 + j*20, 394 - i*56 - size, 16, size), 0)
        screen.blit(Game.gameMenuFont.render('Current wave', 0, menuBaseColor), \
            (784, 425), None, 0)
        screen.blit(Game.gameMenuFont.render('Next waves', 0, menuBaseColor), \
            (784, 117), None, 0)
        self.drawSpeedArrows(screen)
        self.drawSPBtn(screen)
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