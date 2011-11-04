import sys, os, pygame, Game
from Global import *

class Menu():
    def __init__(self, map, wave, towers):
        self.btnStart = StartButton(775,100)
        self.btnRandom = RandomButton(775,450)
        self.btnBack = BackButton(875,450)
        self.btnDino1 = BtnDino1(775,150)
        self.btnDino10 = BtnDino10(875,150)
        self.btnDinoJr2 = BtnDinoJr2(775,200)
        self.btnDinoJr20 = BtnDinoJr20(875,200)
        self.btnNinja5 = BtnNinja5(775,250)
        self.btnNinja50 = BtnNinja50(875,250)
        self.btnPirate5 = BtnPirate5(775,300)
        self.btnPirate50 = BtnPirate50(875,300)
        self.btnSinge10 = BtnSinge10(775,350)
        self.btnSinge100 = BtnSinge100(875,350)
        self.btnExit = ExitButton(775,400)
        self.map = map
        self.wave = wave
        self.towers = towers
        self.menu = pygame.sprite.Group(self.btnStart, self.btnRandom, self.btnBack, self.btnExit)
        self.menu.add(self.btnDino1, self.btnDino10, self.btnDinoJr2, self.btnDinoJr20, self.btnNinja5, self.btnNinja50, self.btnPirate5, self.btnPirate50, self.btnSinge10, self.btnSinge100)

    def draw(self, screen):
        self.menu.draw(screen)

    def onClick(self, pos, map):
        if self.btnStart.rect.collidepoint(pos):
            Game.state = STATE_GAME
        elif self.btnRandom.rect.collidepoint(pos):
            self.wave.clear()
            self.towers.clear()
            map.loadRandomMap()
            self.wave.newRandomSpawn()
            Game.state = STATE_LOADGAME
        elif self.btnBack.rect.collidepoint(pos):
            Game.state = STATE_INITGAMEMENU
        elif self.btnDino1.rect.collidepoint(pos):
            self.wave.clear()
            self.wave.newSpawn(4, 1)
        elif self.btnDino10.rect.collidepoint(pos):
            self.wave.clear()
            self.wave.newSpawn(4, 10)
        elif self.btnDinoJr2.rect.collidepoint(pos):
            self.wave.clear()
            self.wave.newSpawn(3, 2)
        elif self.btnDinoJr20.rect.collidepoint(pos):
            self.wave.clear()
            self.wave.newSpawn(3, 20)
        elif self.btnNinja5.rect.collidepoint(pos):
            self.wave.clear()
            self.wave.newSpawn(0, 5)
        elif self.btnNinja50.rect.collidepoint(pos):
            self.wave.clear()
            self.wave.newSpawn(0, 50)
        elif self.btnPirate5.rect.collidepoint(pos):
            self.wave.clear()
            self.wave.newSpawn(1, 5)
        elif self.btnPirate50.rect.collidepoint(pos):
            self.wave.clear()
            self.wave.newSpawn(1, 50)
        elif self.btnSinge10.rect.collidepoint(pos):
            self.wave.clear()
            self.wave.newSpawn(2, 10)
        elif self.btnSinge100.rect.collidepoint(pos):
            self.wave.clear()
            self.wave.newSpawn(2, 100)
        elif self.btnExit.rect.collidepoint(pos):
            pygame.quit()

class StartButton(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join ('Images\Buttons', 'ok.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class RandomButton(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join ('Images\Buttons', 'A.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
 
class BackButton(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join ('Images\Buttons', 'B.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
 
class BtnDino1(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join ('Images\Buttons', 'Dino1.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
 
class BtnDino10(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join ('Images\Buttons', 'Dino10.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class BtnDinoJr2(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join ('Images\Buttons', 'DinoJr2.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class BtnDinoJr20(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join ('Images\Buttons', 'DinoJr20.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class BtnNinja5(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join ('Images\Buttons', 'Ninja5.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class BtnNinja50(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join ('Images\Buttons', 'Ninja50.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class BtnPirate5(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join ('Images\Buttons', 'Pirate5.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class BtnPirate50(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join ('Images\Buttons', 'Pirate50.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class BtnSinge10(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join ('Images\Buttons', 'Singe10.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class BtnSinge100(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join ('Images\Buttons', 'Singe100.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class ExitButton(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join ('Images\Buttons', 'Quitter.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y