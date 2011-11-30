import os, Game
from Global import *
from math import *
from numpy import *
from numpy.random import *
from Util import *
#from DataTreatment import *
from Evaluate import *


def prog():
    ## une des trois fonctions majeures
    # utilise l'info dans Game.level et Global
    # pour progresser vers une position optimale
    
    ## hyperparametres
    targetVictoryChance = 0.99 # risque d'echouer
    progSteps = 3 # nombre de generations
    efficiencyInsistence = 2 # insistance vers les meilleures tourelles
    propOfKeepingAll = 0.2 # chance de garder les tourelles deja en place
    
    M = Game.level.map.M
    waves = Game.level.levelWaves
    curWave = Game.level.currentWave
    maxWave = Game.level.maxWave
    budgetList = Game.level.levelBudget
    
    totalBudget = 0
    for w in range(curWave+1):
        totalBudget += budgetList[w]
    
    enemy = waves[curWave][0]
    number = waves[curWave][1]
    
    empVal = AemplacementValues(M)
    nbAvEmpInit = len(empVal)
    nbAvEmp = nbAvEmpInit
    avTowers = []
    for avTower in Game.level.levelTowers:
        avTowers.append([avTower])
        
    nbAvTowers = len(avTowers)
    maxUpgrade = 2 # a changer
    nbPossiblePositions = (nbAvTowers * (maxUpgrade+1) + 1) ** nbAvEmp
    # nbPP: facilement des millions
    nbTestPositions = min(10, 100 * int((nbPossiblePositions)**.1))
    testPositions = []
    #towerValues = zeros(6, 3)
    
    ## chances de base de choisir une tourelle
    totalChance = 0
    for i in ind(avTowers):
        avTowers[i].append([])
        for u in range(maxUpgrade):
            chance = 1.0 * TowerStats[avTowers[i][0]][u][12][enemy] ** efficiencyInsistence
            totalChance += chance
            avTowers[i][1].append(chance)
    cumChance = 0
    for tower in avTowers:
        for u in range(maxUpgrade):
            tower[1][u] = 1.0 * tower[1][u] / totalChance
            cumChance += tower[1][u]
            tower[1][u] = cumChance
    
    ## positions de depart (juste une, pour tout de suite)
    startPositions = []
    avBudget = totalBudget
    
    ## tourelles deja placees
    alreadyPlaced = []
    for placedTower in Game.level.towers.towers:
        print '', placedTower.type, placedTower.level
        alreadyPlaced.append([placedTower.type, placedTower.level,
            placedTower.row, placedTower.column, 0.75])
        avBudget -= TowerStats[placedTower.type][placedTower.level][TowerPRICE]
    startPositions.append([avBudget, alreadyPlaced])
    
    #####################
    ##  LOOP EVOLUTIF  ##
    #####################
    
    for progStep in range(progSteps):
        print '\n\n ------------------'
        print '  PROGRESS STEP', progStep
        print ' ------------------'
        print '\n Available start positions:'
        for position in startPositions:
            print ' ', position
        print
        patience = nbTestPositions
        for n in range(nbTestPositions):
            
            nbAvEmp = nbAvEmpInit
            
            ## on choisit une des positions de depart
            randPosNum = randint(0, len(startPositions)-1) \
                if len(startPositions) >= 2 else 0
            print ' Start position chosen:', randPosNum
            avBudget = startPositions[randPosNum][0]
            #print 'Available Budget:', avBudget
            alreadyPlaced = []
            for elem in startPositions[randPosNum][1]:
                alreadyPlaced.append(elem)
            print ' ', alreadyPlaced
            
            ## on garde ou non des tourelles deja placees
            if rand() < propOfKeepingAll:
                nbToKeep = randint(0, len(alreadyPlaced)-1) \
                    if len(alreadyPlaced) >= 2 else 0
                while len(alreadyPlaced) > nbToKeep:
                    indToRemove = randint(0, len(alreadyPlaced)-1) \
                        if len(alreadyPlaced) >= 2 else 0
                    t, u = alreadyPlaced[indToRemove][0], alreadyPlaced[indToRemove][1]
                    chance = 1 - ((1 - TowerStats[t][u][12][enemy]) ** (5 * efficiencyInsistence))
                    if rand() > chance:
                        avBudget += TowerStats[t][u][TowerPRICE] \
                            * alreadyPlaced[indToRemove][4]
                        alreadyPlaced.pop(indToRemove)
            
            budgetLimit = avBudget*(1-rand()**2)
            print ' Budget limit:', budgetLimit
            
            T = [0 for i in range(TowerTYPES)]
            budgetSpent = 0
            while budgetSpent <= budgetLimit and patience and nbAvEmp:
                # on essaie d'ajouter une tourelle, preferant les plus efficaces
                towerChooser = 1.0*rand()
                print ' Random tower chooser:', towerChooser
                t, u = -1, -1
                for tposs, uposs in iter(avTowers, maxUpgrade):
                    #print '', avTowers[tposs]
                    #print '', avTowers[tposs][1]
                    #print '', avTowers[tposs][1][uposs]
                    if towerChooser < avTowers[tposs][1][uposs] \
                        and t == -1 and u == -1:
                        t, u = avTowers[tposs][0], uposs
                        break
                print ' Tower chosen:', t, u
                choiceMade = 0
                if t >= 0 and u >= 0:
                    # on verifie si cette option a un minimum de sens
                    for emp in empVal:
                        if emp[2][t][u]:
                            choiceMade = 1
                            break
                if choiceMade:
                    # ca devrait marcher, on prend en note
                    budgetSpent += TowerStats[t][u][TowerPRICE]
                    T[t*3 + u] += 1 # ajoute a tourelles a essayer de placer
                    nbAvEmp -= 1
                else:
                    # ca a echoue, on perd patience et on recommence
                    patience -= 1
            if budgetSpent <= avBudget:
                # on place cette position le mieux possible
                testTowers = placeTowers(M, T, alreadyPlaced, 1)
                testPositions.append([])
                testPositions[n] = [avBudget, testTowers,
                    posScore(eval(testTowers), avBudget-budgetSpent, targetVictoryChance)]
            print
        
        if testPositions[-1] == []:
            testPositions.remove(testPositions[-1])
        
        ## on garde les meilleures positions selon leur score
        nbKeptPositions = min(len(testPositions), 2*log(len(testPositions)))
        startPositions = []
        while len(startPositions) < (nbKeptPositions):
            bestScore = 0
            bestPosition = 0
            for position in testPositions:
                if position != []:
                    print ' Verifying position:', position
                    score = position[2]
                    if score > bestScore:
                        bestScore = score
                        bestPosition = position
            if bestPosition:
                print ' Best position:', bestPosition
                startPositions.append(bestPosition)
                testPositions.remove(bestPosition)
            else:
                break
    
    #########################
    ##  FIN LOOP EVOLUTIF  ##
    #########################
    
    ## on note la meilleure position
    bestScore = 0
    for position in testPositions:
        if position != []:
            score = position[2]
            if score > bestScore:
                bestScore = score
                bestPosition = position
    
    ## on y fait correspondre le niveau
    # on max le budget
    Game.level.money = totalBudget
    # on efface les tourelles existantes
    Game.level.towers.clear()
    # on place les tourelles choisies
    for chosenTower in bestPosition[1]:
        Game.level.towers.placeTower(chosenTower[0], chosenTower[1],
            chosenTower[2], chosenTower[3])
    # on update le budget
    Game.level.money = bestPosition[0]
    
    
    # choisir et evaluer les tourelles selon les waves a venir aussi?
    # a condition que la wave actuelle reussisse!
    
    
    
    
    
    
    
    