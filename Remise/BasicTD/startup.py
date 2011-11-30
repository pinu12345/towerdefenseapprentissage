import pygame, math, os
pygame.mixer.init()

#Borrowed from pygame tower defence
class Player():
    def __init__(self):
        self.health = 20
        self.BASEHP = self.health
        self.money = 150
        self.BASECASH = self.money
        self.score = 0
        self.wave = 0
        self.enemyCount = 0
        self.diesound = pygame.mixer.Sound(os.path.join ('data', 'laugh.ogg'))
        self.cheerSound = pygame.mixer.Sound(os.path.join ('data', 'cheer.ogg'))

class MapChoice(pygame.sprite.Sprite):
    def __init__(self,x,y,type):
        pygame.sprite.Sprite.__init__(self)

        self.imgLoad()
        self.image = self.imgList[type]
        self.type = type
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.selected = 0

    def imgLoad(self):
        imgbutt = pygame.image.load(os.path.join ('data', 'buttons.png'))

        self.imgList = []

        imgSize = (225, 225)
        offset = ((0, 0), (225,0),(0, 225), (225,225))

        for i in range(4):
            tmpImg = pygame.Surface(imgSize)
            tmpImg.blit(imgbutt, (0, 0), (offset[i], imgSize))
            self.imgList.append(tmpImg)

    def change(self):
        if self.image == self.imgList[self.type]:
            self.image = self.imgList[self.type+2]
            self.selected = 1
        else:
            self.image = self.imgList[self.type]
            self.selected = 0

class ModeButton(pygame.sprite.Sprite):
    def __init__(self,x,y,type):
        pygame.sprite.Sprite.__init__(self)

        self.type = type
        self.imgLoad()
        self.image = self.imgList[0]
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def imgLoad(self):
        if self.type == 0:
            imgbutt = pygame.image.load(os.path.join ('data', 'hardmode.png'))
        else:
            imgbutt = pygame.image.load(os.path.join ('data', 'unlimited.png'))


        self.imgList = []
        if self.type == 0:
            imgSize = (133, 19)
            offset = ((0, 0), (0,19))
        else:
            imgSize = (159, 19)
            offset = ((0, 0), (0,19))

        for i in range(2):
            tmpImg = pygame.Surface(imgSize)
            tmpImg.fill((51,117,20))
            tmpImg.blit(imgbutt, (0, 0), (offset[i], imgSize))
            tmpImg.set_colorkey((51,117,20))
            self.imgList.append(tmpImg)

    def change(self):
        if self.image == self.imgList[0]:
            self.image = self.imgList[1]
        else:
            self.image = self.imgList[0]

class OkButton(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(os.path.join ('data', 'ok.png'))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

def dist(first,second,towerRange):

    aimx,aimy = first

    #This code returns 1 if the tower can shoot anywhere on the map
    if range == 0:
        return 1
    #This code will check the distance and see if the enemy is in range
    #if so, the tower will then be able to shoot it
    elif (math.sqrt((second.centerx-aimx)**2+(second.centery-aimy)**2) <= towerRange):
        return 1

def drawText():
    myFont = pygame.font.SysFont("None", 28)
    pLife = myFont.render("Life: %d"% player.health,1, (255,255,255))
    pScore = myFont.render("Score: %d"% player.score,1, (255,255,255))
    pMoney = myFont.render("Cash: $%d"% player.money,1, (255,255,255))
    pWave = myFont.render("Wave: %d"% player.wave,1, (255,255,255))

    placementx = 665
    placementy = 60
    screen.blit(pLife,(placementx,placementy))
    screen.blit(pScore,(placementx,placementy+25))
    screen.blit(pMoney,(placementx,placementy+50))
    screen.blit(pWave,(placementx,placementy+75))

class Info():
    def __init__(self):
        self.draw = 0
        self.px = 665
        self.py = 340

    def setInfo(self,power,range,upcost,level,type):
        toFont = pygame.font.SysFont("None", 22)
        to1Font = pygame.font.SysFont("None", 30)

        if type == 1:
            self.ttype = toFont.render("Type: Red",1, (255,255,255))
        elif type == 2:
            self.ttype = toFont.render("Type: Green",1, (255,255,255))
        elif type  == 3:
            self.ttype = toFont.render("Type: Blue",1, (255,255,255))
        if level == 3:
            self.tlevel = toFont.render("Level: 3 (Max)",1, (255,255,255))
        else:
            self.tlevel = toFont.render("Level: %d"% level,1, (255,255,255))

        self.tpower = toFont.render("Damage: %d"% power,1, (255,255,255))

        if range != 0:
            self.trange = toFont.render("Range: %d"% range,1, (255,255,255))
        else:
            self.trange = toFont.render("Range: Unlimited",1, (255,255,255))

        self.tupcost = toFont.render("Upgrade Cost: $%d"% upcost,1, (255,255,255))

        if type == 1:
            self.tspeed = toFont.render("Speed: Fast",1, (255,255,255))
        elif type == 2:
            self.tspeed = toFont.render("Speed: Slow",1, (255,255,255))
        elif type  == 3:
            self.tspeed = toFont.render("Speed: Medium",1, (255,255,255))

        if upcost != 0:
            self.uptext = toFont.render("Press U to upgrade",1, (255,255,255))
        else:
            self.uptext = toFont.render("",1, (255,255,255))
        self.draw = 1
    def drawInfo(self):
        if self.draw == 1:
            screen.blit(self.ttype,(self.px,self.py))
            screen.blit(self.tlevel,(self.px,self.py+25))
            screen.blit(self.tpower,(self.px,self.py+50))
            screen.blit(self.trange,(self.px,self.py+75))
            screen.blit(self.tspeed,(self.px,self.py+100))
            screen.blit(self.tupcost,(self.px,self.py+125))
            screen.blit(self.uptext,(self.px,self.py+150))

    def unClick(self):
        self.draw = 0
#This allows easy access in the rest of the code.
player = Player()
info = Info()
baddies = pygame.sprite.Group()
towers = pygame.sprite.Group()

baddieList = list()
towerList = list()
enemyCount = 0

screen = pygame.display.set_mode((825,625))
pygame.display.set_caption("Tower Defense")

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill ((0,0,0))
screen.blit(background, (0,0))

twrSurf = pygame.Surface((625,625))
twrSurf.set_alpha(255*0.4)
twrSurf.fill((255,0,255))
twrSurf.set_colorkey((255,0,255))

drkSurf = pygame.Surface((625,625))
drkSurf.set_alpha(255*0.6)
drkSurf.fill((20,20,20))