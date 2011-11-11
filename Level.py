import sys, os, Level, RandomMap
from Global import *
from random import *
from Util import *

class Level():
    def __init__(self, map, waves, towers, towerBar, menu):
        self.map = map
        self.waves = waves
        self.towers = towers
        self.towerBar = towerBar
        self.menu = menu
        self.resetLevel()
        self.dataLog = []

    def resetLevel(self):
        self.towers.clear()
        self.waves.clear()
        self.levelBudget = 0
        self.levelUpgrades = 0
        self.levelWaves = []
        self.levelTowers = []
        self.levelMap = []
        self.levelMessages = []

        
    def randomLevel(self):
        self.resetLevel()
        # Comment ca, levelBudget? Ca devrait pas etre waveBudget?
        self.levelBudget = 1000000
        self.levelUpgrades = randint(0, 2)
        enemyType = randint(0, len(EnemyStats)-1)
        print "\n Random enemy type:", enemyType
        enemyNumber = randint(1, int(1000/EnemyStats[enemyType][EnemyVALUE]))
        self.levelWaves = [[enemyType, enemyNumber]]
        self.levelTowers = [1, 2, 3, 4, 5, 6]
        self.levelMessages = []
        self.levelMap = RandomMap.RandomMap().M
        self.start()
    
    
    def autoWave(self):
        print "\n\n --- NEW LEVEL (autoWave)---"
        self.resetLevel()
        self.levelBudget = 1000000
        self.levelMap = RandomMap.RandomMap().M
        M = self.levelMap
        
        # Ennemis
        enemyType = randint(0, len(EnemyStats)-1)
        print "\n Enemy type:", EnemyStats[enemyType][EnemyNAME]
        enemyValue = randint(10, 2000)
        print " Target enemy value:", enemyValue
        enemyNumber = randint(1, 
            max(1, int(enemyValue/EnemyStats[enemyType][EnemyVALUE])))
        print " Enemy number:", enemyNumber
        enemyValue = enemyNumber * EnemyStats[enemyType][EnemyVALUE]
        print " Final enemy value:", enemyValue
        
        self.levelWaves = [[enemyType, enemyNumber]]
        self.dataLog.append(str(enemyType))
        self.dataLog.append(str(enemyNumber))
        
        # Tourelles
        self.levelUpgrades = randint(0, 2)
        print "\n Allowed upgrades:", self.levelUpgrades
        usableBudget = randint(2, 10) * enemyValue
        spentBudget = 0
        print " Available budget:", usableBudget
        availableTowers = []
        for i in range(len(TowerStats)):
            if getrandbits(1):
                availableTowers.append(i)
        if sum(availableTowers) == 0:
            availableTowers.append(randint(0, len(TowerStats)-1))
        print " Available towers:",
        for towerNum in availableTowers:
            print TowerStats[towerNum][0][TowerNAME],
        print
        empVal = emplacementValues(M)
        availableEmps = range(len(empVal))
        maxLoop = 0
        while spentBudget < usableBudget and len(availableEmps) > 0:
            maxLoop += 1
            #print ('Placing towers : ', spentBudget, usableBudget, len(availableEmps), maxLoop)
            rEmp = randint(0, len(empVal))
            if rEmp in availableEmps:
                rTower = availableTowers[randint(0, len(availableTowers)-1)]
                rLevel = randint(0, self.levelUpgrades)
                #print ('rEmp', rEmp, rTower, rLevel)
                if empVal[rEmp][2][rTower][rLevel]:
                    #print 'empVal'
                    self.towers.placeTower(map, rTower, rLevel, \
                        empVal[rEmp][0], empVal[rEmp][1])
                    spentBudget += TowerStats[rTower][rLevel][TowerPRICE]
                    availableEmps.remove(rEmp)
                else:
                    if maxLoop > 1000:
                        break
        print('Finished placing towers')

        # Probablement utile
        self.levelTowers = [1, 2, 3, 4, 5, 6]

        # Send the waves
        self.start()

        if Game.state == STATE_PREPARATION: 
            Game.state = STATE_GAME
    
    def loadLevel(self, levelName, levelMap = 'levelMap'):
        self.resetLevel()
        if levelMap != 'levelMap':
            self.levelMap = open(os.path.join('Maps', levelMap + '.txt')).readlines()
        else:
            self.levelFile = open(os.path.join('Maps', levelName+'.txt')).readlines()
        
        for i in range(len(self.levelFile)):
            if i == 1:
                self.levelBudget = int(self.levelFile[i])
            elif i == 4:
                for tower in self.levelFile[i].rsplit(','):
                    type = int(tower.strip())
                    self.levelTowers.append(type)
            elif i == 7:
                self.levelUpgrades = int(self.levelFile[i])
            elif i == 10:
                for wave in self.levelFile[i].rsplit(','):
                    type = wave.strip().rsplit(' ')[0]
                    count = wave.strip().rsplit(' ')[1]
                    self.levelWaves.append([int(type), int(count)])
            elif (i >= 13) and (i <= 28):
                if levelMap == 'levelMap':
                    self.levelMap.append(self.levelFile[i])
            elif i >= 32:
                self.levelMessages.append(self.levelFile[i])
        self.start()
    
    def start(self):
        self.currentWave = 0
        self.maxWave = len(self.levelWaves)
        self.money = self.levelBudget
        self.map.loadMap(self.levelMap)
        ## Verify if there is a message at 0
        if self.levelMessages != []:
            pass
        self.startWave()

    def restart(self):
        self.currentWave = 0
        self.nextWave()
    
    def restartWave(self):
        self.startWave()
    
    def nextWave(self):
        self.currentWave += 1
        ## Verify if there is a message at currentWave
        if self.levelMessages != []:
            pass
        self.startWave()
    
    def startWave(self):
        if self.currentWave < self.maxWave:
            self.waves.newSpawn(self.levelWaves[self.currentWave][0], self.levelWaves[self.currentWave][1])
        else:
            print '\n --- SUCCESS ---\n'
            #print ' '.join(self.dataLog)
            #with open("LearningData.txt", "a") as f:
            #    f.write(' '.join(self.dataLog), "\n")
            #self.randomLevel()
            self.autoWave()