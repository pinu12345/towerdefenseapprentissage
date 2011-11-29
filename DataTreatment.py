import os
from Global import *
from math import *
from numpy import *
from Util import *
from Evaluate import *

def executeTheFollowing():
    #print ' Executing...'
    #treatBalanceData(1) # 1: efface tout et remplace
    #damageAdjustmentTable_average()
    #damageAdjustmentTable_histogram(20)
    #damageAdjustmentTable_neighbor()
    #evalTest()
    damageAdjustmentDataForAnalyticRegression()
    pass

    
def damageAdjustmentTable_neighbor(k = 3):
    pass

def damageAdjustmentTable_parzen():
    pass
    
def damageAdjustmentTable_histogram(k = 3):
    ## renvoie k valeurs d'ajustement pour chaque combo
    ## et le nombre d'ennemis jusqu'auquel elles s'appliquent
    numTowerDA = TowerTYPES*len(EnemyStats)
    TowerDamageAdj = []
    for a in range(numTowerDA):
        TowerDamageAdj.append([])
        for b in range(k):
            TowerDamageAdj[a].append([])
            for c in range(2):
                TowerDamageAdj[a][b].append([])
    for e, t, u in iter(EnemyStats, TowerStats, TowerStats[0]):
        doc = os.path.join('Learning Data', ''.join(map(str, [e, t, u, '.txt'])))
        lines = open(doc).readlines()
        totalShots = [ 0 for a in range(k) ]
        totalDamage = [ 0 for a in range(k) ]
        enemySep = [ 0 for a in range(k) ]
        #totalShots, totalDamage, enemySep = [], [], []
        #for a in range(k):
        #    totalShots.append([])
        #    totalDamage.append([])
        #    enemySep.append([])
        maxEnemyNum = 0
        for i in ind(lines):
            lines[i] = map(float, lines[i].rstrip().split(' '))
            if lines[i][0] > maxEnemyNum:
                maxEnemyNum = float(lines[i][0])
        sort(lines)
        enemySepMult = maxEnemyNum ** (1.0/k)
        last_enemySep = 1
        for c in range(k-1):
            last_enemySep *= enemySepMult
            enemySep[c] = last_enemySep
        enemySep[k-1] = maxEnemyNum
        for i in ind(lines):
            enemyNum = lines[i][0]
            for c in ind(enemySep):
                if enemyNum <= enemySep[c]:
                    totalShots[c] += lines[i][2]
                    totalDamage[c] += lines[i][3]
                    break
        towerBaseDamage = TowerStats[t][u][TowerDAMAGE][e]
        numAdj = e*TowerTYPES + t*len(TowerStats[t]) + u
        for c in range(k-1, -1, -1):
            if totalShots[c]:
                TowerDamageAdj[numAdj][c][0] \
                    = 1.0 * totalDamage[c] / totalShots[c] / towerBaseDamage
            else:
                TowerDamageAdj[numAdj][c][0] = TowerDamageAdj[numAdj][c+1][0]
            TowerDamageAdj[numAdj][c][1] = enemySep[c]
    for i in ind(TowerDamageAdj):
        for j in ind(TowerDamageAdj[i]):
            TowerDamageAdj[i][j] = '|'.join(map(str, TowerDamageAdj[i][j]))
        TowerDamageAdj[i] = ' '.join(TowerDamageAdj[i])
    with open(os.path.join('Learning Data', 'DAhistogram.txt'), 'w') as f:
        for line in TowerDamageAdj:
            #print '', line
            f.write(''.join([line, "\n"]))
    return TowerDamageAdj

    
def damageAdjustmentDataForAnalyticRegression():
    ## prepare des fichiers pour la regression analytique
    ## chaque ligne comprend le nombre d'ennemis et l'ajustement de degats
    for e, t, u in iter(EnemyStats, TowerStats, TowerStats[0]):
        doc = os.path.join('Learning Data', ''.join(map(str, [e, t, u, '.txt'])))
        lines = open(doc).readlines()
        towerBaseDamage = TowerStats[t][u][TowerDAMAGE][e]
        data = []
        for i in ind(lines):
            line = lines[i].split(' ')
            success = int(line[4].rstrip())
            if success:
            #if 1:
                enemyNum = int(line[0])
                realShots = int(line[2])
                realDamage = float(line[3])
                estimDamage = 1.0 * realShots * towerBaseDamage
                adjDamage = 1.0 * realDamage / estimDamage
                if e == 0 and t == 0 and u == 0:
                    print '', realDamage, estimDamage
                data.append(' '.join([str(enemyNum), str(adjDamage)]))
        doc = os.path.join('Learning Data', ''.join(map(str, [e, t, u, 'a.txt'])))
        with open(doc, 'w') as f:
            for line in data:
                f.write(''.join([line, "\n"]))
    print '\n All done!\n'
    
    
def damageAdjustmentTable_average():
    ## renvoie une unique valeur d'ajustement pour chaque combo
    ## l'ecrit egalement dans DAaverage.txt
    TowerDamageAdj = [0] * (TowerTYPES*len(EnemyStats))
    for e, t, u in iter(EnemyStats, TowerStats, TowerStats[0]):
        doc = os.path.join('Learning Data', ''.join(map(str, [e, t, u, '.txt'])))
        lines = open(doc).readlines()
        totalShots = 0
        totalDamage = 0
        for i in range(len(lines)):
            lines[i] = map(float, lines[i].rstrip().split(' '))
        for i in range(len(lines)):
            totalShots += lines[i][2]
            totalDamage += lines[i][3]
        #print '', t, u, e
        #print '', TowerStats[t][u][TowerDAMAGE][e]'
        #print '', totalShots, '\n'
        damageAdj = 1.0 * totalDamage / totalShots \
            / TowerStats[t][u][TowerDAMAGE][e]
        TowerDamageAdj[e*TowerTYPES + t*len(TowerStats[t]) + u] \
            = damageAdj
    print
    for i in ind(TowerDamageAdj):
        print '', i/TowerTYPES, i%TowerTYPES/len(TowerStats[0]), \
            i%TowerTYPES%len(TowerStats[0]), '', '%.2f'%(TowerDamageAdj[i])
    print
    with open(os.path.join('Learning Data', 'DAaverage.txt'), 'w') as f:
        for line in TowerDamageAdj:
            f.write(''.join([str(line), "\n"]))
    return TowerDamageAdj
    #print "\n Damage adjustments calculated\n"


def treatBalanceData(startFromScratch):
    if startFromScratch:
        resetBalanceData()
    textData = open(os.path.join('BalanceData.txt')).readlines()
    for n in range(len(textData)):
        splitData = textData[n].rstrip().split(' ')
        # 0     1      2     3       4      5     6      7
        # enemy number tower upgrade number shots damage success
        e, t, u = splitData[0], splitData[2], splitData[3]
        for i in range(7, -1, -1):
            if i in [0, 2, 3]:
                splitData.pop(i)
        treatedData = ' '
        with open(''.join(["Learning Data/", \
            e, t, u, ".txt"]), "a") as f:
            f.write(''.join([' '.join(splitData), "\n"]))
    minDataLen = inf
    for n in range(TowerTYPES*len(EnemyStats)):
        doc = ''.join([str(n/TowerTYPES), str(n%TowerTYPES/len(TowerStats[0])), \
            str(n%TowerTYPES%len(TowerStats[0])), '.txt'])
        textData = open(os.path.join('Learning Data', doc)).readlines()
        for i in range(len(textData)-1, -1, -1):
            textData[i] = textData[i].split(' ')
            if int(textData[i][1]) == 0:
                textData.pop(i)
        dataLen = len(textData)
        print '', doc, dataLen
        if dataLen <  minDataLen:
            minDataLen = dataLen
    print '\n All balance data treated: minimum', minDataLen, 'per combo'

def resetEnemyLearningData():
    for enemyType in range(len(EnemyStats)):
        open(''.join(["Enemy Learning Data/ELD", \
            str(enemyType), ".txt"]), 'w').close()
    print "\n Enemy learning data reset"

def resetBalanceData():
    for e in range(len(EnemyStats)):
        for t in range(len(TowerStats)):
            for u in range(len(TowerStats[t])):
                open(''.join(["Learning Data/", str(e), \
                    str(t), str(u), ".txt"]), 'w').close()
    print "\n Treated Learning data reset\n"

def treatLearningData():
    textData = open(os.path.join('LearningData.txt')).readlines()

    LData = [[] for i in range(len(EnemyStats))]

    # [ Soldat[], Moto[], Buggy[], ... ]
    #   [ Wave1testee[], Wave2testee[], ... ]
    #     [ Nombre, Tourelles[], Succes ]
    #       [ Tourelle1[], Tourelle2[], ... ]
    #         [ Type, Niveau, ValeurEmp ]

    for n in range(len(textData)):
        splitWave = textData[n].split('|')
        enemyTextData = splitWave[0].split(',')
        enemy = int(enemyTextData[0])
        number = int(enemyTextData[1])
        towerData = splitWave[1].split(';')
        towerEffect = [0] * TowerTYPES
        for i in range(len(towerData)):
            towerData[i] = towerData[i].split(',')
            for j in range(len(towerData[i])):
                towerData[i][j] = int(towerData[i][j])
            tower, level = towerData[i][0], towerData[i][1]
            reach = towerData[i][2]
            delay = TowerStats[tower][level][TowerDELAY]
            damage = TowerStats[tower][level][TowerDAMAGE][enemy]
            speed = EnemyStats[enemy][EnemySPEED]
            spread = EnemyStats[enemy][EnemySPREAD]
            nbShots = ceil(((number-1)*1.0*spread+reach) / (speed*delay))
            effect = nbShots * damage / (10000 * number)
            towerEffect[tower*3+level] += effect
        for i in range(len(towerEffect)):
            towerEffect[i] = str(towerEffect[i])
        success = int(splitWave[2].rstrip())
        towerEffect.insert(0, str(number))
        towerEffect.append(str(success))
        with open(''.join(["Enemy Learning Data/ELD", \
            str(enemy), ".txt"]), "a") as f:
            f.write(''.join([','.join(towerEffect), "\n"]))

    print "\n All enemy learning data treated"
        #LData[enemy].append([number, towerData, success])
        
    #for i in range(2):
    #    print LData[0][i]
    
executeTheFollowing()