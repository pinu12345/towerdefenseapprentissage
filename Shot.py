from Global import *
from Util import *
import pygame

class Shot(pygame.sprite.Sprite):
    def __init__(self, xi, yi, xt, yt, type):
        pygame.sprite.Sprite.__init__(self)
        
        self.type = type
        self.xi = xi
        self.yi = yi
        self.xt = xt
        self.yt = yt
        
        if TowerShotGraphs[type][1] > 0:
            self.projAlpha = 255
            self.projColor = TowerShotGraphs[type][0]
            self.projDecay = 255 // TowerShotGraphs[type][1]
            self.projWidth = TowerShotGraphs[type][2]
        else:
            self.projAlpha = 0
        if TowerShotGraphs[type][4] > 0:
            self.zoneAlpha = 255
            self.zoneColor = TowerShotGraphs[type][3]
            self.zoneDecay = 255 // TowerShotGraphs[type][4]
            self.zoneRadius = TowerTypes[type][TowerSPLASH][0]
        else:
            self.zoneAlpha = 0
        
    def draw(self, screen):
        if self.projAlpha <= 0 and self.zoneAlpha <= 0:
            self.kill()
        if self.projAlpha > 0:
            self.projColorAlpha = ( \
                self.projColor[0], self.projColor[1], self.projColor[2], \
                self.projAlpha)
            pygame.draw.line(screen, \
                self.projColorAlpha, \
                (self.xi + tileSize/2-1, self.yi + tileSize/2-1), \
                (self.xt + tileSize/2-1, self.yt + tileSize/2-1), \
                self.projWidth)
            pygame.draw.circle(screen, \
                self.projColorAlpha, \
                (self.xi + tileSize/2, self.yi + tileSize/2), \
                self.projWidth*2 + 2)
            pygame.draw.circle(screen, \
                self.projColorAlpha, \
                (self.xt + tileSize/2, self.yt + tileSize/2), \
                self.projWidth*2 + 2)
            self.projAlpha -= 1000
        if self.zoneAlpha > 0:
            self.zoneColorAlpha = ( \
                self.zoneColor[0], self.zoneColor[1], self.zoneColor[2], \
                self.zoneAlpha)
            pygame.draw.circle(screen, \
                self.zoneColorAlpha, \
                (self.xt + tileSize/2, self.yt + tileSize/2), \
                self.zoneRadius * tileSize + 4)
            self.zoneAlpha -= 1000
