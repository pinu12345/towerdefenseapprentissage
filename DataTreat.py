import os
from Global import *


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
    enemyType = int(enemyTextData[0])
    enemyNumber = int(enemyTextData[1])
    towerData = splitWave[1].split(';')
    for i in range(len(towerData)):
        towerData[i] = towerData[i].split(',')
        for j in range(len(towerData[i])):
            towerData[i][j] = int(towerData[i][j])
    success = int(splitWave[2].rstrip())
    LData[enemyType].append([enemyNumber, towerData, success])
    
for i in range(1):
    print LData[0][i]