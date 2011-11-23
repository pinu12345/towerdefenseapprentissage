import sys, os, pygame, Enemy, Tower
from Global import *
from random import *
from Util import *

class Towers():
    def __init__(self, map, wave):
        self.map = map
        self.towers = pygame.sprite.Group()
        self.wave = wave

    def placeTower(self, towerType, towerLevel, row, column):
        #Enleve la valeur de la tour au budget
        Game.level.updateMoney(-100)
        addedTower = Tower.Tower(row, column, towerType, towerLevel, self.map)
        self.towers.add(addedTower)
        self.map.T[row][column] = addedTower

    def eraseTower(self, row, column):
        #Rembourse 75% de la valeur de la tour
        Game.level.updateMoney(75)
        currentTower = self.map.T[row][column]
        currentTower.resetEmplacement()
        currentTower.kill()
        self.map.T[row][column] = 0

    def updateTower(self, towerType, row, column):
        currentTower = self.map.T[row][column]
        if (towerType == TowerUPGRADE) or (towerType == currentTower.type):
            #Enleve la valeur de la tour au budget
            Game.level.updateMoney(-100)
            currentTower.upgrade()
        else:
            #Rembourse 75% de la valeur de la tour
            Game.level.updateMoney(75)
            #Enleve la valeur de la tour au budget
            Game.level.updateMoney(-100)
            currentTower.resetEmplacement()
            currentTower.kill()
            addedTower = Tower.Tower(row, column, towerType, 0, self.map)
            self.towers.add(addedTower)
            self.map.T[row][column] = addedTower
    
    def placeTowers(self, M, T):
        # T: dimension 18, contient le nombre a construire de chaque tourelle
        empVal = AemplacementValues(M)
        emp_available = len(empVal)
        nbPlaced = 0
        toPlace = []
        beenPlaced = []
        for i in range(len(T)):
            iOrder = TowerPlaceOrder[i]
            iToPlace = T[iOrder]
            for n in range(iToPlace):
                toPlace.append(iOrder)
        for num in toPlace:
            t = num / 3
            l = num % 3
            if emp_available:
                bestEmpValue = 0
                for emp in empVal:
                    if emp[2][t][l] > bestEmpValue:
                        bestEmp = emp
                        bestEmpValue = emp[2][t][l]
                if bestEmpValue:
                    emp = bestEmp
                    emp_available -= 1
                    empVal.remove(emp)
                    self.placeTower(M, t, l, emp[0], emp[1])
                    beenPlaced.append(num)
        Tplaced = [0 for i in range(len(T))]
        for num in beenPlaced:
            Tplaced[num] += 1
        return Tplaced
    
    def target(self, shots):
        for tower in self.towers:
            tower.target(self.wave.enemies, shots)

    def drawRadioactivity(self, screen):
        for tower in self.towers:
            if tower.type == 5:
                tower.drawRadioactivity(screen)

    def draw(self, screen):
        for tower in self.towers:
            tower.draw(screen)

    def resetCooldowns(self):
        for tower in self.towers:
            tower.firing = 0
            tower.cooldown = 0

    def clear(self):
        Game.placedTower = 1
        self.map.clearTowers()
        for tower in self.towers:
            tower.resetEmplacement()
        self.towers.empty()
