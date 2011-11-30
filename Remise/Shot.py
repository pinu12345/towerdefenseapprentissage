from Global import *
from Util import *
import pygame

class Shot(pygame.sprite.Sprite):
    def __init__(self, xi, yi, xt, yt, type, level, card):
        pygame.sprite.Sprite.__init__(self)
        
        self.xi = xi
        self.yi = yi
        self.xt = xt
        self.yt = yt
        self.type = type
        self.level = level
        self.card = card
        self.offset = ShotGraphs[type][ShotOFFSET]*2
        
        if ShotGraphs[type][ShotWIDTH] > 0:
            self.projAlpha = 255
            self.projColor = ShotGraphs[type][ShotCOLOR]
            self.projDecay = 255
            self.projWidth = ShotGraphs[type][ShotWIDTH]
        else:
            self.projAlpha = 0
        if ShotGraphs[type][ShotZONECOLOR] > 0:
            self.zoneAlpha = 255
            self.zoneColor = ShotGraphs[type][3]
            self.zoneFarColor = ShotGraphs[type][3]
            self.zoneDecay = 255
            self.zoneRadius = TowerStats[type][level][TowerSPLASH]
        else:
            self.zoneAlpha = 0
        
    def draw(self, screen):
        if self.projAlpha <= 0 and self.zoneAlpha <= 0:
            self.kill()
        if self.projAlpha > 0:
            self.projColorAlpha = ( \
                self.projColor[0], self.projColor[1], self.projColor[2], \
                self.projAlpha)
            xiOff, yiOff = self.xi, self.yi
            coOff = self.offset
            if self.card == cardN:
                yiOff = self.yi - coOff
            elif self.card == cardS:
                yiOff = self.yi + coOff
            elif self.card == cardW:
                xiOff = self.xi - coOff
            elif self.card == cardE:
                xiOff = self.xi + coOff
            else:
                coOff = int(round(.707*coOff))
                if self.card == cardNW:
                    xiOff = self.xi - coOff
                    yiOff = self.yi - coOff
                elif self.card == cardNE:
                    xiOff = self.xi + coOff
                    yiOff = self.yi - coOff
                elif self.card == cardSW:
                    xiOff = self.xi - coOff
                    yiOff = self.yi + coOff
                elif self.card == cardSE:
                    xiOff = self.xi + coOff
                    yiOff = self.yi + coOff
            
            pygame.draw.line(screen, \
                self.projColorAlpha, \
                (xiOff + tileSize/2-1, yiOff + tileSize/2-1), \
                (self.xt + tileSize/2-1, self.yt + tileSize/2-1), \
                self.projWidth)
            pygame.draw.circle(screen, \
                self.projColorAlpha, \
                (xiOff + tileSize/2, yiOff + tileSize/2), \
                self.projWidth*2 + 1)
            pygame.draw.circle(screen, \
                self.projColorAlpha, \
                (self.xt + tileSize/2, self.yt + tileSize/2), \
                self.projWidth*2 + 1)
            self.projAlpha -= 1000
        if self.zoneAlpha > 0:
            self.zoneColorAlpha = ( \
                self.zoneColor[0], self.zoneColor[1], self.zoneColor[2], \
                self.zoneAlpha)
            self.zoneFarColorAlpha = ( \
                self.zoneFarColor[0], self.zoneFarColor[1], self.zoneFarColor[2], \
                self.zoneAlpha)
            #pygame.draw.circle(screen, \
            #    self.zoneFarColorAlpha, \
            #    (self.xt + tileSize/2, self.yt + tileSize/2), \
            #    self.zoneRadius + 4)
            pygame.draw.circle(screen, \
                self.zoneColorAlpha, \
                (self.xt + tileSize/2, self.yt + tileSize/2), \
                self.zoneRadius/2 + 2)
            self.zoneAlpha -= 1000
