import sys, os, pygame, Enemy, Tower
from Global import *
from random import *
from Util import *

class Towers():
    def __init__(self, map, wave):
        self.map = map
        self.towers = pygame.sprite.Group()
        self.wave = wave

    def placeTower(self, map, towerType, towerLevel, row, column):
        addedTower = Tower.Tower(row, column, towerType, towerLevel, self.map)
        self.towers.add(addedTower)
        self.map.T[row][column] = addedTower

    def updateTower(self, map, towerType, towerLevel, row, column):
        currentTower = map.T[row][column]
        if towerType == currentTower.type:
            currentTower.upgrade()
        else:
            currentTower.resetEmplacement()
            currentTower.kill()
            addedTower = Tower.Tower(row, column, towerType, towerLevel, self.map)
            self.towers.add(addedTower)
            map.T[row][column] = addedTower
    
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

    def draw(self, screen):
        for tower in self.towers:
            tower.draw(screen)

    def resetCooldowns(self):
        for tower in self.towers:
            tower.firing = 0
            tower.cooldown = 1
            

    def clear(self):
        Game.placedTower = 1
        self.map.clearTowers()
        for tower in self.towers:
            tower.resetEmplacement()
        self.towers.empty()
