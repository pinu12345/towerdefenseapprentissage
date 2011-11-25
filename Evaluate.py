import os, Game
from Global import *
from math import *
from numpy import *
from Util import *
from DataTreatment import *


method_average = 0
method_histogram = 1
method_neighbor = 2
best_method = 2


def eval(chosenTowers):
    ## une des trois fonctions majeures
    # chosenTowers est une liste dont chaque element
    # est une tourelle [tower, upgrade, y, x]
    enemy = Game.level.waves[currentWave][0]
    number = Game.level.waves[currentWave][0]    
    speed = EnemyStats[enemy][EnemySPEED]
    spread = EnemyStats[enemy][EnemySPREAD]
    totalDamage = 0
    for chosenTower in chosenTowers:
        towerData = map(int, chosenTower.split(','))
        t, u, y, x = towerData[0], towerData[1], towerData[2], towerData[3]
        reach = AsingleTowerEmpValue(Game.level.map.M, y, x, t, u)
        delay = TowerStats[t][u][TowerDELAY]
        nbShots = ceil((1.0*(number-1)*spread+reach) / (speed*delay))
        damage = TowerStats[t][u][TowerDAMAGE][enemy]
        damageA = 1.0*damage / 10000 \
            * damageAdjustment(TowerDA, enemy, number, t, u, method)
        totalDamage += nbShots * damageA
    killProp = 1.0*totalDamage / number * enemyAdjustment(enemy, number, method)
    sucGuess = 0 if killProp < 1 else 1
    if sucGuess:
        print "\n I think you'll win.\n"
    else:
        print "\n I think you'll lose.\n"
    return sucGuess
    
    
def evalTest(method = best_method):
    TowerDA = getDamageAdjustmentTable(method)
    textData = open(os.path.join('LearningData.txt')).readlines()
    nbErrors = 0
    errorSize = 0
    nbSpecificError = 0
    specificEnemyValue = 0
    optimistErrors = 0
    pessimistErrors = 0
    checkedTower = 5
    checkedTowerErrors = 0
    checkedTowerCases = 0
    nbTestPos = len(textData)
    #nbTestPos = 5
    print
    for n in range(nbTestPos):
    #for n in range(75, 80):
        onlyCheckedTower = 1
        splitWave = textData[n].rstrip().split('|')
        enemyTextData = splitWave[0].split(',')
        enemy = int(enemyTextData[0])
        number = int(enemyTextData[1])
        speed = EnemyStats[enemy][EnemySPEED]
        spread = EnemyStats[enemy][EnemySPREAD]
        allTowerData = splitWave[1].split(';')
        cumDamage = 0
        for placedTower in allTowerData:
            towerData = map(int, placedTower.split(','))
            t, u, = towerData[0], towerData[1]
            if t != checkedTower:
                onlyCheckedTower = 0
            reach = towerData[2]
            delay = TowerStats[t][u][TowerDELAY]
            nbShots = ceil((1.0*(number-1)*spread+reach) \
                / (speed*delay))
            damage = TowerStats[t][u][TowerDAMAGE][enemy]
            #print TowerDA[enemy*TowerTYPES + t*len(TowerStats[t]) + u]
            #print damageAdjustment(TowerDA, enemy, number, t, u, method)
            damageA = 1.0*damage / 10000 \
                * damageAdjustment(TowerDA, enemy, number, t, u, method)
            cumDamage += nbShots * damageA
        if onlyCheckedTower:
            checkedTowerCases += 1
        killProp = 1.0*cumDamage / number * enemyAdjustment(enemy, number, method)
        sucGuess = 0 if killProp < 1 else 1
        sucKnown = int(splitWave[2])
        #print '', sucKnown, '%.2f'%(killProp), ' wave', n
        if (sucKnown != sucGuess):
            if onlyCheckedTower:
                checkedTowerErrors += 1
            ## en cas d'erreur
            nbErrors += 1
            errorSize += max(killProp, 1/killProp) -1
            #print '', sucKnown, sucGuess, '%.2f'%(killProp), ' wave', (n+1), \
            #    ' enemy', enemy, ' number', number
            if sucKnown == 0:
                nbSpecificError += 1
                specificEnemyValue += number
                #print '', sucKnown, '%.2f'%(killProp), ' wave', (n+1), \
                #    ' enemy', enemy, ' number', number, \
                #    ' enemy value', number*EnemyStats[enemy][EnemyVALUE]
                for placedTower in allTowerData:
                    towerData = map(int, placedTower.split(','))
                    t, u, = towerData[0], towerData[1]
            if sucGuess:
                optimistErrors += 1
            else:
                pessimistErrors += 1
    averageSpecEnemyValue = 1.0*specificEnemyValue/nbSpecificError
    print '\n Average enemy number:', averageSpecEnemyValue
    predRate = 1.0 - 1.0*nbErrors / nbTestPos
    print '\n Prediction rate:', '%.2f'%(100*predRate), '%'
    averageError = 1.0*errorSize / nbErrors if nbErrors else 0
    print '\n Average error when wrong:', '%.2f'%(100*averageError), '%'
    print '\n Optimistic errors:', optimistErrors
    print ' Pessimistic errors:', pessimistErrors
    checkedTowerName = TowerStats[checkedTower][0][TowerNAME]
    print '\n Checked tower:', checkedTower, checkedTowerName
    print ' Checked tower positions:', checkedTowerCases
    checkedTowerPredRate = 1.0 - 1.0*checkedTowerErrors/checkedTowerCases
    print ' Checked tower prediction rate:', '%.2f'%(100*checkedTowerPredRate), '%'
    

def enemyAdjustment(e, n, method = best_method):
    avEnemyNumber = [48.2, 10.8, 4.6, 14.9, 4.5, 5.3, 3.9, 3.6, 2.0]
    
    if method == method_histogram:
        return 1.045*(avEnemyNumber[e]*1.0/n)**.2
    
    elif method == method_neighbor:
        return 1.03
    
    else:
        return 1

    
def damageAdjustment(TowerDA, e, n, t, u, method = best_method):
    numAdj = e*TowerTYPES + t*len(TowerStats[t]) + u
    
    if method == method_average:
        return TowerDA[numAdj]
    
    elif method == method_histogram:
        maxTDA = len(TowerDA[0])
        #print '', n,
        for s in range(maxTDA):
            #print '%.2f'%(TowerDA[numAdj][s][1]),
            if n <= TowerDA[numAdj][s][1]:
                #print
                #print ' On y echappe!'
                return TowerDA[numAdj][s][0]
        #print
        return TowerDA[numAdj][maxTDA-1][0]
    
    elif method == method_neighbor:
        normalDamage = TowerStats[t][u][TowerDAMAGE][e]
        area = TowerDA[numAdj]
        nbNeighbors = len(area)
        totalWeight = 0
        totalDamageAdj = 0
        for neighbor in area:
            if neighbor[2] > 0:
                weight = min(1.0*n/neighbor[0], 1.0*neighbor[0]/n) **2
                totalWeight += weight
                totalDamageAdj += weight * (neighbor[3] / neighbor[2] / normalDamage)
        damageAdj = 1.0 * totalDamageAdj / totalWeight
        return damageAdj
    
    elif method == method_parzen:
        pass
        


def getDamageAdjustmentTable(method = best_method):

    if method == method_average:
        doc = os.path.join('Learning Data', 'DAaverage.txt')
        lines = open(doc).readlines()
        #numTowerDA = TowerTYPES*len(EnemyStats)
        #TowerDA = [0] * (numTowerDA)
        for i in ind(lines):
            lines[i] = float(lines[i].rstrip())
    
    elif method == method_histogram:
        doc = os.path.join('Learning Data', 'DAhistogram.txt')
        lines = open(doc).readlines()
        #numTowerDA = TowerTYPES*len(EnemyStats)
        #TowerDA = [0] * (numTowerDA)
        for i in ind(lines):
            lines[i] = lines[i].rstrip().split(' ')
            for j in ind(lines[i]):
                lines[i][j] = map(float, lines[i][j].split('|'))
    
    elif method == method_neighbor:
        ## renvoie toute l'information connue
        numTowerDA = TowerTYPES*len(EnemyStats)
        TowerDamageAdj = []
        for a in range(numTowerDA):
            TowerDamageAdj.append([])
        for e, t, u in iter(EnemyStats, TowerStats, TowerStats[0]):
            numAdj = e*TowerTYPES + t*len(TowerStats[t]) + u
            doc = os.path.join('Learning Data', ''.join(map(str, [e, t, u, '.txt'])))
            lines = open(doc).readlines()
            for i in ind(lines):
                lines[i] = map(float, lines[i].rstrip().split(' '))
            for i in ind(lines):
                TowerDamageAdj[numAdj].append(lines[i])
            #if numAdj == 1:
                #print TowerDamageAdj[numAdj]
        lines = TowerDamageAdj
    
    return lines
    
    
TowerDA = getDamageAdjustmentTable(method)