import pygame, os

class Tower(pygame.sprite.Sprite):
    def __init__(self, xy, type):
        pygame.sprite.Sprite.__init__(self)
        towerList.append(self)

        x, y = xy
        self.level = 1

        self.imgList = None
        self.loadImages()

        self.type = type

        #Your Normal Cheap Tower
        if self.type == 1:
            self.image = self.imgList[0]
            self.BASEDMG = 7
            self.damage = self.BASEDMG
            self.cost = 70
            self.range = 100
            self.reload = 15
            self.reloadNum = 0
            self.upcost = 50

        #Strong, but slow tower
        else:
            self.image = self.imgList[3]
            self.BASEDMG = 20
            self.damage = self.BASEDMG
            self.range = 75
            self.reload = 60
            self.reloadNum = 0
            self.upcost = 80

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.surfx, self.surfy = self.rect.center
        self.surfx -= 100
        self.surfy -= 100

    def update(self):
        i = 1

    def loadImages(self):
        imgMaster = pygame.image.load(os.path.join ('Images', 'towers.png'))

        self.imgList = []

        imgSize = (25, 25)
        offset = ((0, 0), (25,0), (50,0),(0, 25), (25,25), (50,25),(0, 50), (25,50), (50,50))

        for i in range(9):
            tmpImg = pygame.Surface(imgSize)
            tmpImg.blit(imgMaster, (0, 0), (offset[i], imgSize))
            self.imgList.append(tmpImg)

    def target(self):
        for enemy in baddieList:
            aimx = enemy.rect.centerx
            aimy = enemy.rect.bottom - 13
            if self.range == 0:
                enemy.health -= self.damage
                return (aimx,aimy)
            elif dist((aimx,aimy),self.rect,self.range) == 1:
                enemy.health -= self.damage
                return (aimx,aimy)

class TowerIcons(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)

        self.imgList = None
        self.loadImages()

        self.type = type

        #Your Normal Cheap Tower
        if self.type == 1:
            self.image = self.imgList[0]
            self.BASEDMG = 7
            self.cost = 50
            self.range = 100
            self.speed = 'fast'

        #Strong, but slow tower
        else:
            self.image = self.imgList[1]
            self.BASEDMG = 20
            self.cost = 75
            self.range = 75
            self.speed = 'Slow'

        self.rect = self.image.get_rect()

        self.rect.centerx = x
        self.rect.y = y
        self.daFont = pygame.font.SysFont("None", 20)

    def loadImages(self):
        imgMaster = pygame.image.load(os.path.join ('Images', 'towers.png'))

        self.imgList = []

        imgSize = (25, 25)
        offset = ((0, 0),(0, 25),(0, 50))

        for i in range(3):
            tmpImg = pygame.Surface(imgSize)
            tmpImg.blit(imgMaster, (0, 0), (offset[i], imgSize))
            self.imgList.append(tmpImg)

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.txtDraw()

    def txtDraw(self):
        tdamage = self.daFont.render("Base Damage: %d"% self.BASEDMG,1, (255,255,255))
        if self.range != 0:
            trange = self.daFont.render("Range: %d"% self.range,1, (255,255,255))
        else:
            trange = self.daFont.render("Range: Unlimited",1, (255,255,255))
        tcost = self.daFont.render("Cost: $%d"% self.cost,1, (255,255,255))
        tspeed = self.daFont.render("Speed: " + self.speed,1, (255,255,255))

        placementx = 665
        placementy = 230

        screen.blit(tdamage,(placementx,placementy))
        screen.blit(trange,(placementx,placementy+25))
        screen.blit(tcost,(placementx,placementy+50))
        screen.blit(tspeed,(placementx,placementy+75))