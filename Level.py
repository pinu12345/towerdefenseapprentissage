import sys, os, Level, RandomMap
from Global import *
from random import *
from Util import *

class Level():
    def __init__(self, map, waves, towers, towerBar, menu):
        self.resetLevel()
        self.map = map
        self.waves = waves
        self.towers = towers
        self.towerBar = towerBar
        self.menu = menu

    def resetLevel(self):
        self.levelBudget = 0
        self.levelUpgrades = 0
        self.levelWaves = []
        self.levelTowers = []
        self.levelMap = []
        
    def randomLevel(self):
        self.resetLevel()
        self.levelBudget = 9999
        self.levelUpgrades = 2
        self.levelWaves = [[0, 5], [1, 5], [2, 5], [3, 5], [4, 5], [5, 5], [6, 5], [7, 5], [8, 5]]
        self.levelTowers = [1, 2, 3, 4, 5, 6]
        self.levelMap = RandomMap.RandomMap().M
        self.start()

    def loadLevel(self, levelName, levelMap = 'levelMap'):
        self.resetLevel()
        if levelMap != 'levelMap':
            self.levelMap = open(os.path.join('Maps', levelMap + '.txt')).readlines()
        else:
            self.levelFile = open(os.path.join('Maps', levelName+'.txt')).readlines()
        for i in range(len(self.levelFile)):
            if i == 1:
                self.levelBudget = int(self.levelFile[i])
            if i == 4:
                for tower in self.levelFile[i].rsplit(','):
                    type = int(tower.strip())
                    self.levelTowers.append(type)
            if i == 7:
                self.levelUpgrades = int(self.levelFile[i])
            if i == 10:
                for wave in self.levelFile[i].rsplit(','):
                    type = wave.strip().rsplit(' ')[0]
                    count = wave.strip().rsplit(' ')[1]
                    self.levelWaves.append([int(type), int(count)])
            if levelMap == 'levelMap':
                if i >= 13:
                    self.levelMap.append(self.levelFile[i])
        self.start()
    
    def start(self):
        self.currentWave = 0
        self.maxWave = len(self.levelWaves)
        self.money = self.levelBudget
        self.map.loadMap(self.levelMap)
        self.nextWave()

    def restart(self):
        self.currentWave = 0
        self.nextWave()
    
    def nextWave(self):
        if self.currentWave < self.maxWave:
            self.waves.newSpawn(self.levelWaves[self.currentWave][0], self.levelWaves[self.currentWave][1])
            self.currentWave += 1
        else:
            print 'Level complete, congratulations!'