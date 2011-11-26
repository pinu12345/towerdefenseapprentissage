import os, Game
from Global import *
from math import *
from numpy import *
from numpy.random import *
from Util import *
#from DataTreatment import *


method_average = 0
method_histogram = 1
method_neighbor = 2
best_method = 1


def eval(chosenTowers, method = best_method):
    ## une des trois fonctions majeures
    # chosenTowers est une liste dont chaque element
    # est une tourelle [tower, upgrade, y, x]
    currentWave = Game.level.currentWave
    enemy = Game.level.levelWaves[currentWave][0]
    number = Game.level.levelWaves[currentWave][1]
    speed = EnemyStats[enemy][EnemySPEED]
    spread = EnemyStats[enemy][EnemySPREAD]
    totalDamage = 0
    for towerData in chosenTowers:
        t, u, y, x = towerData[0], towerData[1], towerData[2], towerData[3]
        reach = AsingleTowerEmpValue(Game.level.map.M, y, x, t, u)
        delay = TowerStats[t][u][TowerDELAY]
        nbShots = ceil((1.0*(number-1)*spread+reach) / (speed*delay))
        damage = TowerStats[t][u][TowerDAMAGE][enemy]
        damageA = 1.0*damage / 10000 \
            * damageAdjustment(TowerDA, enemy, number, t, u, method)
        totalDamage += nbShots * damageA
    killProp = 1.0*totalDamage / number
    print 'killProp:', killProp
    #killProp = 1.0*totalDamage / number * enemyAdjustment(enemy, number, method)
    victChan = evalVictoryChances(killProp)
    print 'victChan:', victChan
    printComment(victChan)
    return victChan
    

def evalVictoryChances(killProp):
    ## transforme la proportion de kills en garantie concrete de non-defaite
    # presentement, simple conversion tanh basee sur resultats empiriques
    return tanh(1.7 * killProp ** 1.6)

    
def posScore(victChan, budgetLeft, targetVictoryChance, needToWin = 1):
    ## plus needToWin est eleve, plus on maximise les chances de victoire
    ## si la victoire est improbable, on penche vers victChan
    # victChan vient d'eval et est parmi [0, 1]
    # budgetLeft est calcule dans prog
    # needToWin depend eventuellement de l'etape de progression et est parmi [0, 1]
    # targetVictoryChance est un hyperparametre de prog
    if victChan >= targetVictoryChance:
        return 1 + budgetLeft
    else:
        return victChan


def evalPlayerPosition():
    playerTowers = Game.level.towers.towers
    if len(playerTowers) == 0:
        print "\n You can't win with no tower, that's for sure.\n"
    else:
        alreadyPlaced = []
        for playerTower in playerTowers:
            alreadyPlaced.append([playerTower.type, playerTower.level,
                playerTower.y, playerTower.x])
        eval(alreadyPlaced)
        

def printComment(victChan):
    if victChan > 0.99:
        victoryTexts = [
            "\n That's a guranteed win!\n",
            "\n I'm totally sure you'll win.\n",
            "\n You can't lose with that!\n",
            "\n I'm 100% sure you'll win.\n"]
        print victoryTexts[randint(0, 3)]
    elif victChan < 0.01:
        victoryTexts = [
            "\n That's a definite loss.\n",
            "\n I'm totally sure you'll lose.\n",
            "\n No way you can win with that!\n",
            "\n You're kidding me, right?\n"]
        print victoryTexts[randint(0, 3)]
    elif victChan > 0.6:
        textChance = '%.2f'%(victChan*100)
        victoryTexts = [
            ' '.join(["\n There's a", textChance, "% chance you'll win.\n"]),
            ' '.join(["\n I evaluate your chances of winning at", textChance, "%.\n"]),
            ' '.join(["\n You might win; there's a", textChance, "% chance of it.\n"]),
            ' '.join(["\n Chances of winning are evaluated at", textChance, "%.\n"])]
        print victoryTexts[randint(0, 3)]
    elif victChan < 0.4:
        textChance = '%.2f'%(victChan*100)
        victoryTexts = [
            ' '.join(["\n There's a paltry", textChance, "% chance you'll win.\n"]),
            ' '.join(["\n I evaluate your chances of winning at barely", textChance, "%.\n"]),
            ' '.join(["\n You'll probably lose; there's only a", textChance, "% chance you'll win.\n"]),
            ' '.join(["\n Chances of winning are evaluated at a puny", textChance, "%.\n"])]
        print victoryTexts[randint(0, 3)]
    else:
        textChance = '%.2f'%(victChan*100)
        victoryTexts = [
            ' '.join(["\n There's barely a", textChance, "% chance you'll win.\n"]),
            ' '.join(["\n I evaluate your chances of winning at", textChance, "%.\n"]),
            "\n You might win, you might lose.\n",
            "\n Winning and losing seem equally probable.\n"]
        print victoryTexts[randint(0, 3)]
    
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
    
    
TowerDA = getDamageAdjustmentTable(best_method)