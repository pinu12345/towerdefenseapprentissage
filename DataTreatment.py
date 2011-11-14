import os
from Global import *
from math import *

resetEnemyLearningData = 1
print "\n Enemy learning data reset"
if resetEnemyLearningData:
    for enemyType in range(len(EnemyStats)):
        open(''.join(["Enemy Learning Data/ELD", \
            str(enemyType), ".txt"]), 'w').close()

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