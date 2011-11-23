import pygame, Map, os, Images, Game, random
from Global import *

# Colors
selected = (205, 149, 12)

class TowerBar():
    def __init__(self, origX, origY):
        self.origX = origX
        self.origY = origY
        self.space = 8
        self.towerCount = len(Images.TowerImages)
        self.selectedTower = -1
        self.redraw = 1
        self.updateMoney = 1

    def moneyUpdated(self, screen):
        screen.blit(Game.gameMenuFont.render('Money', 0, (255, 255, 255)), (294, 569), None, 0)
        screen.blit(Game.gameMenuFont.render(str(Game.level.money), 0, (255, 255, 255)), (294, 590), None, 0)
        self.updateMoney = 0

    # Dessine les tours dans la barre
    #  Si une tour est selectionner dessine un arriere plan en or
    #  Sinon dessine un arriere plan noir
    def draw(self, screen):
        upgradeX = self.origX + 150
        upgradeY = self.origY + 26
        eraseX = self.origX + 150
        eraseY = self.origY + 64
        if self.selectedTower == TowerUPGRADE:
            self.showUpgrade(screen)
            screen.blit(Images.InterfaceBGbright, (upgradeX, upgradeY) , (upgradeX, upgradeY, tileSize, tileSize), 0)
            screen.blit(Images.InterfaceBGwashed, (eraseX, eraseY) , (eraseX, eraseY, tileSize, tileSize), 0)
        elif self.selectedTower == TowerERASE:
            self.showNothing(screen)
            screen.blit(Images.InterfaceBGwashed, (upgradeX, upgradeY) , (upgradeX, upgradeY, tileSize, tileSize), 0)
            screen.blit(Images.InterfaceBGbright, (eraseX, eraseY) , (eraseX, eraseY, tileSize, tileSize), 0)
        else:
            screen.blit(Images.InterfaceBGwashed, (eraseX, eraseY) , (eraseX, eraseY, tileSize, tileSize), 0)
            screen.blit(Images.InterfaceBGwashed, (upgradeX, upgradeY) , (upgradeX, upgradeY, tileSize, tileSize), 0)
        for i in range(self.towerCount):
            drawX = self.origX + ((i%(self.towerCount/2)) * (tileSize + self.space)) + 16
            drawY = self.origY + (i/3 * (tileSize + self.space)) + 24
            if i == self.selectedTower:
                screen.blit(Images.InterfaceBGbright, (drawX, drawY) , (drawX, drawY, tileSize, tileSize), 0)
                screen.blit(Images.TowerImages[i][0], (drawX , drawY), None, 0)
                self.showTower(screen, i)
            else:
                if i in Game.level.levelTowers:
                    screen.blit(Images.InterfaceBGwashed, (drawX, drawY) , (drawX, drawY, tileSize, tileSize), 0)
                    screen.blit(Images.TowerImages[i][0], (drawX, drawY), None, 0)
                else:
                    screen.blit(Images.InterfaceBGwashed, (drawX, drawY) , (drawX, drawY, tileSize, tileSize), 0)
        self.moneyUpdated(screen)
        self.redraw = 0

    def showNothing(self, screen):
        screen.blit(Images.InterfaceBGwashed, (196, 512) , (196, 512, 796, 116), 0)

    def showUpgrade(self, screen):
        screen.blit(Images.InterfaceBGwashed, (196, 512) , (196, 512, 796, 116), 0)

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


    def onClick(self, pos):
        #6 Towers
        x = (pos[0] - self.origX - 16) // (tileSize + self.space)
        y = (pos[1] - self.origY - 24) // (tileSize + self.space)
        if (x >= 0) and (x < 3):
            if (y >= 0) and (y < 2):
                if (x+(3*y)) in Game.level.levelTowers:
                    self.selectTower(x+(3*y))
        #Upgrade and erase
        elif (pos[0] >= self.origX + 150) and (pos[0] <= self.origY + 178):
            if (pos[1] >= self.origY + 27) and (pos[1] <= self.origY + 54):
                self.selectTower(TowerUPGRADE)
            elif (pos[1] >= self.origY + 66) and (pos[1] <= self.origY + 94):
                self.selectTower(TowerERASE)

    def selectTower(self, tower):
        self.selectedTower = tower
        self.redraw = 1