import os
from Global import *
from math import *
from numpy import *

def executeTheFollowing():
    #print ' Executing...'
    #treatBalanceData(1) # 1: efface tout et remplace
    analyzeBalanceData()

def analyzeBalanceData():
    #print ' Analyzing...'
    Adj = [] * (TowerTYPES*len(EnemyStats))
    for e in range(len(EnemyStats)):
        for t in range(len(TowerStats)):
            for u in range(len(TowerStats[t])):
                doc = ''.join(map(str, ['Learning Data/', e, t, u, '.txt']))
                lines = open(os.path.join(doc)).readlines()
                totalShots = 0
                totalShots2 = 0
                totalDamage = 0
                totalDamage2 = 0
                for line in lines:
                    line = map(float, line.rstrip().split(' '))
                ihalf = len(lines) / 2
                
                    totalShots += splitLine[2]
                    totalDamage += splitLine[3]
                damageAdj = 1.0 * totalDamage / totalShots \
                    / TowerStats[t][u][TowerDAMAGE][e]
                print '', e, t, u, '', round(damageAdj, 2)
                #Adj[e*TowerTYPES +
    print "\n Damage adjustments calculated\n"


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
    print "\n All balance data treated\n"

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
            effect = ceil(((number-1)*spread+reach) \
                / (speed*delay)) * damage / (10000 * number)
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