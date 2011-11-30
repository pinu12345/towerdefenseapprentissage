import pygame, Map, os, Images, Game, random, Util
from Global import *

# Colors
selected = (205, 149, 12)

class TowerBar():
    def __init__(self, origX, origY, map, towers):
        self.towers = towers
        self.map = map
        self.origX = origX
        self.origY = origY
        self.space = 8
        self.towerCount = len(Images.TowerImages)
        self.updateTowerCost = 0
        self.selectedTower = -1
        self.redraw = 1
        self.updateMoney = 1
        self.displayTowerLevel = -1
        self.displayTower = -1

    # Dessine les tours dans la barre
    def draw(self, screen):
        upgradeX = self.origX + 150
        upgradeY = self.origY + 26
        eraseX = self.origX + 150
        eraseY = self.origY + 64
        screen.blit(Images.InterfaceBGwashed, (0, mapHeight*tileSize), (0, mapHeight*tileSize, 194, bottomMenuSize))
        if self.selectedTower == TowerUPGRADE:
            screen.blit(Images.InterfaceBGbright, (upgradeX, upgradeY) , (upgradeX, upgradeY, tileSize, tileSize), 0)
            screen.blit(Images.InterfaceBGwashed, (eraseX, eraseY) , (eraseX, eraseY, tileSize, tileSize), 0)
        elif self.selectedTower == TowerERASE:
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
            else:
                if i in Game.level.levelTowers:
                    screen.blit(Images.InterfaceBGwashed, (drawX, drawY) , (drawX, drawY, tileSize, tileSize), 0)
                    screen.blit(Images.TowerImages[i][0], (drawX, drawY), None, 0)
                else:
                    screen.blit(Images.InterfaceBGwashed, (drawX, drawY) , (drawX, drawY, tileSize, tileSize), 0)
        self.redraw = 0

    def showWashed(self, screen):
        screen.blit(Images.InterfaceBGwashed, (196, 512) , (196, 512, 796, 116), 0)
    
    def showOpaque(self, screen):
        screen.blit(Images.InterfaceBGopaque, (196, 512) , (196, 512, 796, 116), 0)

    def moneyUpdated(self, screen):
        bgx, bgy, bgw, bgh = 280, 530, 183, 22
        screen.blit(Images.InterfaceBGopaque, (bgx, bgy) , (bgx, bgy, bgw, bgh), 0)
        screen.blit(Game.gameMenuFont.render('Materials:', \
            0, menuBaseColor), (296, 527), None, 0)
        screen.blit(Game.gameMenuFont.render(str(int(Game.level.money)), \
            0, menuBaseColor), (318, 553), None, 0)
        self.updateMoney = 0

    def showTower(self, screen):
        bgx, bgy, bgw, bgh = 280, 552, 183, 24
        screen.blit(Images.InterfaceBGopaque, (bgx, bgy) , (bgx, bgy, bgw, bgh), 0)
        if self.displayTower > -1:
            #Show the Tower
            screen.blit(Images.InterfaceBGopaque, (196, 512) , (196, 512, 796, 116), 0)
            x = 206
            y = 524
            screen.blit(pygame.transform.scale2x(Images.TowerImages[self.displayTower][0]), (x, y), None, 0)
            screen.blit(Images.InterfaceLevels[self.displayTowerLevel], (x + 48, y + 68), None, 0)
            for i in range(len(Images.EnemyImages)):
                size = TowerStats[self.displayTower][self.displayTowerLevel][11][i]
                screen.fill(barColor, (654 + i*36, 574 - size, 28, size), 0)
                screen.blit(Images.EnemyImages[i], (652 + i*36, 576), (0, 0, tileSize, tileSize), 0)
            for j in range(4):
                size = TowerStats[self.displayTower][self.displayTowerLevel][7+j]
                screen.fill(barColor, (478 + j*40, 574 - size, 28, size), 0)
            #Show the Price
            if(self.updateTowerCost == 2):
                screen.blit(Game.gameMenuFont.render('Max level', \
                    0, menuMaxLevelColor), (294, 587), None, 0)
            elif(self.updateTowerCost == 3):
                sellInfo = ' '.join(['Sell:', str(int(0.75 * Util.calcTowerPrice( \
                    self.displayTower, self.displayTowerLevel)))])
                screen.blit(Game.gameMenuFont.render(sellInfo, \
                    0, menuSellColor), (294, 587), None, 0)
            else:
                priceInfo = ' '.join(['Price:', str(TowerStats[self.displayTower][self.displayTowerLevel][TowerPRICE])])
                screen.blit(Game.gameMenuFont.render(priceInfo, \
                    0, menuBaseColor), (294, 587), None, 0)
        else:
            self.showWashed(screen)
        self.moneyUpdated(screen)
        self.updateTowerCost = 0

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
        Game.updateUnderMouse(self.map, self, self.towers)
        self.redraw = 1