from Global import *
from Util import *
import pygame

class Shot:
    def __init__(self, xi, yi, xt, yt, type):
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
            self.zoneRadius = TowerTypes[type][TowerSPLASH]
        else:
            self.zoneAlpha = 0
        
    def draw(self, screen):
        if self.projAlpha <= 0 and self.zoneAlpha <= 0:
            # remove shot?
            pass
        if self.projAlpha > 0:
            self.projColorAlpha = ( \
                self.projColor[0], self.projColor[1], self.projColor[2], \
                self.projAlpha)
            pygame.draw.aaline(screen, \
                self.projColorAlpha, \
                (self.xi + tileSize/2, self.yi + tileSize/2), \
                (self.xt + tileSize/2, self.yt + tileSize/2), \
                200)
            #self.projAlpha -= self.projDecay
            self.projAlpha -= 1000
        if self.zoneAlpha > 0:
            self.zoneColorAlpha = ( \
                self.zoneColor[0], self.zoneColor[1], self.zoneColor[2], \
                self.zoneAlpha)
            pygame.draw.circle(screen, \
                self.projColorAlpha, \
                (self.xi + tileSize/2, self.yi + tileSize/2), \
                self.zoneRadius)
            #self.zoneAlpha -= self.zoneDecay
            self.zoneAplha -= 1000
