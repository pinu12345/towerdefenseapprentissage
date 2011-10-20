import pygame, os
from startup import *


class NormalEnemy(pygame.sprite.Sprite):
    def __init__(self,wave, waypoints, mode):
        pygame.sprite.Sprite.__init__(self)

        baddieList.append(self)
        baddies.add(self)
        player.enemyCount +=1

        self.reward = 5
        self.points = 150
        self.speed = 4
        self.health = wave*5+5

        self.wait = 3
        self.node = 1
        self._S, self._E, self._0, self._1, self._2, self._3,\
        self._4, self._5, self._6, self._7, self._8, self._9 = waypoints

        self.loadImages()

        self.frame = 0
        self.delay = 2
        self.pause = 0

        self.image = self.imgList[0]
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = self._S

        self.node_x, self.node_y = self._0
        self.result = {0: self._S, 1: self._0, 2: self._1, 3: self._2,
             4: self._3, 5: self._4, 6: self._5, 7: self._6, 8: self._7,
             9: self._8,10: self._9, 11: self._E
            }
        self.d = 0
        if mode == 'hard':
            self.health *= 2
            self.reward *=2

        self.starthealth = self.health
        self.distance = 0


    def update(self):
        if self.health <= 0:
            player.score += self.points
            player.money += self.reward
            player.diesound.play()
            self.kill()
            baddieList.remove(self)
            player.enemyCount -=1
        self.animate()
        self.move()

    def move(self):

        #Checks to see if there is going to be overshooting of the node
        if ((self.node_x - self.speed) < self.rect.centerx) and self.d == 1:
            self.rect.centerx = self.node_x
        if ((self.node_y - self.speed) < self.rect.centery) and self.d == 2:
            self.rect.centery = self.node_y

        if ((self.node_x + self.speed) > self.rect.centerx) and self.d == 3:
            self.rect.centerx = self.node_x
        if ((self.node_y + self.speed) > self.rect.centery) and self.d == 4:
            self.rect.centery = self.node_y

        #Normal movement
        if self.rect.centerx < self.node_x:
            self.rect.centerx += self.speed
            self.d=1
        if self.rect.centery < self.node_y:
            self.rect.centery += self.speed
            self.d=2

        if self.rect.centerx > self.node_x:
            self.rect.centerx -= self.speed
            self.d=3
        if self.rect.centery > self.node_y:
            self.rect.centery -= self.speed
            self.d=4

        #setting the next node
        if (self.rect.centerx == self.node_x) and (self.rect.centery == self.node_y):
            if self.node < 11:
                self.node += 1
                self.node_x, self.node_y = self.result[self.node]
            else:
                self.wait -=1
                if self.wait <= 0:
                    player.health -= 1
                    player.cheerSound.play()
                    self.kill()
                    baddieList.remove(self)
                    player.enemyCount -=1
        self.distance += self.speed

    def loadImages(self):
        imgMaster = pygame.image.load(os.path.join ('data', 'normEnemy.png'))

        self.imgList = []

        imgSize = (30, 25)
        offset = ((0, 0), (32,0), (63,0), (93,0), (125,0), (156,0), (187,0), (218,0), (248,0), (280,0))

        for i in range(10):
            tmpImg = pygame.Surface(imgSize)
            tmpImg.blit(imgMaster, (0, 0), (offset[i], imgSize))
            transColor = tmpImg.get_at((1, 1))
            tmpImg.set_colorkey(transColor)
            self.imgList.append(tmpImg)

    def animate(self):
        self.pause += 1
        if self.pause >= self.delay:
            self.pause = 0
            self.frame += 1
            if self.frame >= len(self.imgList):
                self.frame = 0

            self.image = self.imgList[self.frame]
            #self.rect = self.image.get_rect()

class HardEnemy(pygame.sprite.Sprite):
    def __init__(self,wave, waypoints, mode):
        pygame.sprite.Sprite.__init__(self)

        baddieList.append(self)
        baddies.add(self)
        player.enemyCount +=1

        self.reward = 500
        self.points = 1000
        self.speed = 1
        self.health = (wave)*400

        self.wait = 1
        self.node = 1
        self._S, self._E, self._0, self._1, self._2, self._3,\
        self._4, self._5, self._6, self._7, self._8, self._9 = waypoints

        self.loadImages()

        self.frame = 0
        self.delay = 3
        self.pause = 0

        #self.image = pygame.image.load(os.path.join ('data', 'hardEnemy_base.png'))
        self.image = self.imgList[0]
        self.rect = self.image.get_rect()

        self.rect.centerx, self.rect.bottom = self._S #self.rect.centery
        self.rect.bottom +=13

        self.node_x, self.node_y = self._0
        self.result = {0: self._S, 1: self._0, 2: self._1, 3: self._2,
             4: self._3, 5: self._4, 6: self._5, 7: self._6, 8: self._7,
             9: self._8,10: self._9, 11: self._E
            }
        self.d = 0
        if mode == 'hard':
            self.health *=2
            self.reward *=2

        self.starthealth = self.health
        self.distance = 0


    def update(self):
        if self.health <= 0:
            player.score += self.points
            player.money += self.reward
            player.diesound.play()
            self.kill()
            player.enemyCount -=1
            baddieList.remove(self)
        self.move()
        self.animate()

    def move(self):

        superx = self.rect.centerx
        #supery = self.rect.centery
        supery = self.rect.bottom - 13

        #Checks to see if there is going to be overshooting of the node
        if ((self.node_x - self.speed) < superx) and self.d == 1:
            superx = self.node_x
        if ((self.node_y - self.speed) < supery) and self.d == 2:
            supery = self.node_y

        if ((self.node_x + self.speed) > superx) and self.d == 3:
            superx = self.node_x
        if ((self.node_y + self.speed) > supery) and self.d == 4:
            supery = self.node_y

        #Normal movement
        if superx < self.node_x:
            superx += self.speed
            self.d=1
        if supery < self.node_y:
            supery += self.speed
            self.d=2

        if superx > self.node_x:
            superx -= self.speed
            self.d=3
        if supery > self.node_y:
            supery -= self.speed
            self.d=4

        self.rect.centerx = superx
        self.rect.bottom = supery + 13
##        self.rect.centery = supery

##        print(self.node)
##        print(self.d)

        #setting the next node
        if (superx == self.node_x) and (supery == self.node_y):
            if self.node < 11:
                self.node += 1
                self.node_x, self.node_y = self.result[self.node]
            else:
                self.wait -=1
                if self.wait <= 0:
                    player.health -= 10
                    player.cheerSound.play()
                    self.kill()
                    baddieList.remove(self)
                    player.enemyCount -=1
        self.distance += self.speed

    def loadImages(self):
        imgMaster = pygame.image.load(os.path.join ('data', 'hardEnemy.png'))

        self.imgList = []

        imgSize = (45, 98)
        offset = ((0, 0), (45,0),(90,0),(135,0),(180,0))

        for i in range(5):
            tmpImg = pygame.Surface(imgSize)
            tmpImg.blit(imgMaster, (0, 0), (offset[i], imgSize))
            transColor = tmpImg.get_at((1, 1))
            tmpImg.set_colorkey(transColor)
            self.imgList.append(tmpImg)

    def animate(self):
        self.pause += 1
        if self.pause >= self.delay:
            self.pause = 0
            self.frame += 1
            if self.frame >= len(self.imgList):
                self.frame = 0
            if (self.d == 1) or (self.d == 4):
                self.image = pygame.transform.flip(self.imgList[self.frame], 1, 0)
            else:
                self.image = self.imgList[self.frame]

class WeakEnemy(pygame.sprite.Sprite):
    def __init__(self,wave, waypoints, mode):
        pygame.sprite.Sprite.__init__(self)

        baddieList.append(self)
        baddies.add(self)
        player.enemyCount +=1

        self.reward = 4
        self.points = 75
        self.speed = 7
        self.health = wave*3+4

        self.wait = 1
        self.node = 1
        self.distance = 0
        self._S, self._E, self._0, self._1, self._2, self._3,\
        self._4, self._5, self._6, self._7, self._8, self._9 = waypoints

        self.loadImages()

        self.frame = 0
        self.delay = 4
        self.pause = 0

        self.image = self.imgList[0]
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = self._S
        self.node_x, self.node_y = self._0
        self.result = {0: self._S, 1: self._0, 2: self._1, 3: self._2,
             4: self._3, 5: self._4, 6: self._5, 7: self._6, 8: self._7,
             9: self._8,10: self._9, 11: self._E
            }
        self.d = 0
        if mode == 'hard':
            self.health *= 2
            self.reward *= 2

        self.starthealth = self.health


    def update(self):
        if self.health <= 0:
            player.score += self.points
            player.money += self.reward
            player.diesound.play()
            self.kill()
            baddieList.remove(self)
            player.enemyCount -=1
        self.move()
        self.animate()

    def move(self):

        #Checks to see if there is going to be overshooting of the node
        if ((self.node_x - self.speed) < self.rect.centerx) and self.d == 1:
            self.rect.centerx = self.node_x
        if ((self.node_y - self.speed) < self.rect.centery) and self.d == 2:
            self.rect.centery = self.node_y

        if ((self.node_x + self.speed) > self.rect.centerx) and self.d == 3:
            self.rect.centerx = self.node_x
        if ((self.node_y + self.speed) > self.rect.centery) and self.d == 4:
            self.rect.centery = self.node_y

        #Normal movement
        if self.rect.centerx < self.node_x:
            self.rect.centerx += self.speed
            self.d=1
        if self.rect.centery < self.node_y:
            self.rect.centery += self.speed
            self.d=2

        if self.rect.centerx > self.node_x:
            self.rect.centerx -= self.speed
            self.d=3
        if self.rect.centery > self.node_y:
            self.rect.centery -= self.speed
            self.d=4

        #setting the next node
        if (self.rect.centerx == self.node_x) and (self.rect.centery == self.node_y):
            if self.node < 11:
                self.node += 1
                self.node_x, self.node_y = self.result[self.node]
            else:
                self.wait -=1
                if self.wait <= 0:
                    player.health -= 1
                    player.cheerSound.play()
                    self.kill()
                    baddieList.remove(self)
                    player.enemyCount -=1
        self.distance += self.speed

    def loadImages(self):
        imgMaster = pygame.image.load(os.path.join ('data', 'weakEnemy.png'))

        self.imgList = []

        imgSize = (26, 27)
        offset = ((0, 0), (26,0))

        for i in range(2):
            tmpImg = pygame.Surface(imgSize)
            tmpImg.blit(imgMaster, (0, 0), (offset[i], imgSize))
            transColor = tmpImg.get_at((1, 1))
            tmpImg.set_colorkey(transColor)
            self.imgList.append(tmpImg)

    def animate(self):
        self.pause += 1
        if self.pause >= self.delay:
            self.pause = 0
            self.frame += 1
            if self.frame >= len(self.imgList):
                self.frame = 0
            if (self.d == 3) or (self.d == 2):
                self.image = pygame.transform.flip(self.imgList[self.frame], 1, 0)
            else:
                self.image = self.imgList[self.frame]

            #self.rect = self.image.get_rect()
