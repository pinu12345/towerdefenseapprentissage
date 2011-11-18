import sys, os, Level, RandomMap, Global
from Global import *
from Util import *
from random import *
from math import *

class Level():
    def __init__(self, map, waves, towers, towerBar, menu):
        self.map = map
        self.waves = waves
        self.towers = towers
        self.towerBar = towerBar
        self.resetLevel()
        self.dataLog = ''
        self.BSTEP = 0
        self.BTNUMBER = 1
        self.BEINDEX = 0
        self.BCONTINUE = 1

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
        #print '\n\n --- Random Level --- \n'
        self.resetLevel()
        # Comment ca, levelBudget? Ca devrait pas etre waveBudget?
        self.levelBudget = 1000000
        self.levelUpgrades = randint(0, 2)
        enemyType = randint(0, len(EnemyStats)-1)
        #print "\n Random enemy type:", enemyType
        enemyNumber = randint(1, int(1000/EnemyStats[enemyType][EnemyVALUE]))
        self.levelWaves = [[enemyType, enemyNumber]]
        self.levelTowers = [0, 1, 2, 3, 4, 5]
        self.levelMessages = []
        self.levelMap = RandomMap.RandomMap().M
        self.start()

    def autoWave(self):
        print "\n\n --- Automatic Wave Start ---"
        Game.speedModifier = 100000
        self.resetLevel()
        self.levelBudget = 1000000
        self.levelMap = RandomMap.RandomMap().M
        M = self.levelMap
        P = precisePathMap(M)
        print " --- Map generated ---"
        
        # Ennemis
        enemyType = randint(0, len(EnemyStats)-1)
        #print "\n Enemy type:", EnemyStats[enemyType][EnemyNAME]
        enemyValue = randint(10, 2000)
        #print " Target enemy value:", enemyValue
        enemyNumber = randint(1, 
            max(1, int(enemyValue/EnemyStats[enemyType][EnemyVALUE])))
        #print " Enemy number:", enemyNumber
        enemyValue = enemyNumber * EnemyStats[enemyType][EnemyVALUE]
        #print " Final enemy value:", enemyValue
        
        self.levelWaves = [[enemyType, enemyNumber]]
        self.dataLog = ','.join([str(enemyType), str(enemyNumber)])
        print " --- Enemies chosen ---"
        
        # Tourelles
        self.levelUpgrades = randint(0, 2)
        #print "\n Allowed upgrades:", self.levelUpgrades
        usableBudget = randint(1, 8) * enemyValue
        spentBudget = 0
        #print " Available budget:", usableBudget
        print " --- Determining available towers ---"
        availableTowers = []
        for i in range(len(TowerStats)):
            if getrandbits(1):
                availableTowers.append(i)
        if sum(availableTowers) == 0:
            availableTowers.append(randint(0, len(TowerStats)-1))
        #print " Available towers:",
        #for towerNum in availableTowers:
            #print TowerStats[towerNum][0][TowerNAME],
        #print
        print " --- Calculating emplacement values ---"
        empVal = emplacementValues(M, P)
        availableEmps = range(len(empVal))
        print ' --- Starting tower placement ---'
        maxLoop = 0
        towerDataLog = ''
        self.start()
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
                    towerDataLog = ';'.join([towerDataLog, ','.join([str(rTower), str(rLevel), str(empVal[rEmp][2][rTower][rLevel])])])
                else:
                    if maxLoop > 200:
                        break
        #print self.dataLog
        self.dataLog = '|'.join([self.dataLog, towerDataLog[1:]])
        #print(' Finished placing towers')
        print " --- Automatic Wave End ---\n"

    def balanceWave(self):
        Global.BalanceWAVE += 1
        print '\n Balance Wave ', Global.BalanceWAVE
        Game.speedModifier = 2500
        self.resetLevel()
        self.levelBudget = 1000000
        #self.levelMap = open(os.path.join('Maps', 'BalanceMap.txt')).readlines()
        #self.levelMap = open(os.path.join('Maps', 'testmap.txt')).readlines()
        self.levelMap = RandomMap.RandomMap().M
        M = self.levelMap
        P = precisePathMap(M)
        
        ## Ennemis
        #enemyType = 0
        enemyType = randint(0, 8)
        #benum = range(enemyStep, enemyStep*9, enemyStep)
        #enemyStep = 4
        enemyValue = EnemyStats[enemyType][EnemyVALUE]
        enemyBudget = randint(1, 1000)
        #enemyBudget = randint(10, 20)
        #enemyNumber = benum[self.BEINDEX]
        enemyNumber = int(ceil(enemyBudget/enemyValue))
        enemyBudget = enemyNumber * enemyValue
        self.levelWaves = [[enemyType, enemyNumber]]
        #self.dataLog = ','.join([str(enemyType), str(enemyNumber)])
        self.dataLog = [str(enemyType), str(enemyNumber)]
        
        ## Tourelles
        #bTower = 0
        bTower = randint(0, 5)
        #bLevel = 0
        bLevel = randint(0, 2)
        #brows = range(13, \
        #    max(0, 12-TowerStats[bTower][bLevel][TowerRANGE]//tileSize), -1)
        #bcols = [11, 12, 10, 13, 9, 14, 8, 15]
        #bcols = [11, 12, 10, 13]
        #towerDataLog = ''
        self.start()
        if 0:
            #for n in range(self.BTNUMBER):
            #    self.towers.placeTower(map, bTower, bLevel, brows[self.BSTEP], bcols[n])
            #    sTEV = singleTowerEmpValue(P, brows[self.BSTEP], bcols[n], bTower, bLevel)
            #    #print sTEV
            #    towerDataLog = ';'.join([towerDataLog, ','.join([ \
            #        str(bTower), str(bLevel), str(sTEV)])])
            #if self.BTNUMBER < len(bcols):
            #    self.BTNUMBER += 1
            #elif self.BEINDEX < len(benum)-1:
            #    self.BEINDEX += 1
            #elif self.BSTEP < len(brows)-1:
            #    self.BTNUMBER = 1
            #    self.BEINDEX = 0
            #    self.BSTEP += 1
            #else:
            #    self.BCONTINUE = 0
            pass
        #print ' --- Starting tower placement ---'
        #empList = emplacementList(M)
        #availableEmps = range(len(empList))
        #maxLoop = 0
        #usableBudget = (10**random()-1) * enemyBudget
        #print usableBudget
        ## Formule magique
        reach = max(1.5*TowerStats[bTower][bLevel][TowerRANGE], \
            TowerStats[bTower][bLevel][TowerSPLASH]/2)
        delay = TowerStats[bTower][bLevel][TowerDELAY]
        damage = TowerStats[bTower][bLevel][TowerDAMAGE][enemyType]
        speed = EnemyStats[enemyType][EnemySPEED]
        spread = EnemyStats[enemyType][EnemySPREAD]
        effect = ceil(((enemyNumber-1)*1.0*spread+reach) / (speed*delay))
        adjustedDamage = 1.0 / max(1, ceil(10000/damage))
        calcTowerNumber = 1.0*enemyNumber / (effect * adjustedDamage)
        randTowerNumber = int((4**random()-1) * 1.0*calcTowerNumber)
        print '\n Enemies:', enemyNumber, '\n Reach:', reach, '\n Effect:', effect, "\n Damage'", adjustedDamage, '\n Towers:', randTowerNumber
        T = [0] * TowerTYPES
        T[3*bTower+bLevel] = int(randTowerNumber)
        #T[3*bTower+bLevel] = int(ceil(usableBudget/TowerStats[bTower][bLevel][TowerPRICE]))
        T = self.towers.placeTowers(M, T)
        self.dataLog.extend([bTower, bLevel, T[3*bTower+bLevel]])
        self.start()
        #self.dataLog = ','.join(self.dataLog)
    
    def loadLevel(self, levelName, levelMap = 'levelMap'):
        self.resetLevel()
        if levelMap != 'levelMap':
            self.levelMap = open(os.path.join('Maps', levelMap + '.txt')).readlines()
        else:
            self.levelFile = open(os.path.join('Maps', levelName + '.txt')).readlines()
        
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
        #self.logWave(1)
        self.startWave()
    
    def logWave(self, success):
        #if success:
            #print '\n --- SUCCESS ---\n'
        #else:
            #print '\n --- FAILURE ---\n'
        self.dataLog.extend([Global.DataSHOTS, Global.DataDAMAGE, success])
        Global.DataSHOTS, Global.DataDAMAGE = 0, 0
        self.dataLog = ' '.join(map(str, self.dataLog))
        if Game.balanceMode:
            with open("BalanceData.txt", "a") as f:
                f.write(''.join([self.dataLog, "\n"]))
        elif Game.autoMode:
            with open("LearningData.txt", "a") as f:
                f.write(''.join([self.dataLog, "\n"]))
        #self.randomLevel()
    
    def startWave(self):
        if self.currentWave < self.maxWave and self.BCONTINUE:
            self.waves.newSpawn(self.levelWaves[self.currentWave][0], self.levelWaves[self.currentWave][1])
        elif Game.autoMode:
            self.autoWave()
        elif Game.balanceMode:
            if self.BCONTINUE:
                self.balanceWave()
            else:
                print '\n Balance test over; quitting.\n'
                sys.exit()
        else:
            print '\n Game finished; quitting.\n'
            sys.exit()