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
    nbAvEmp = len(empVal)
    avTowers = []
    for avTower in Game.level.levelTowers:
        avTowers.append([avTower])
        
    nbAvTowers = len(avTowers)
    maxUpgrade = 2 # a changer
    nbPossiblePositions = (nbAvTowers * (maxUpgrade+1) + 1) ** nbAvEmp
    # nbPP: facilement des millions
    nbTestPositions = min(2, 100 * int((nbPossiblePositions)**.1))
    testPositions = []
    #towerValues = zeros(6, 3)
    
    ## chances de base de choisir une tourelle
    totalChance = 0
    for i in ind(avTowers):
        avTowers[i].append([])
        for u in range(maxUpgrade):
            chance = TowerStats[avTowers[i][0]][u][12][enemy] ** efficiencyInsistence
            totalChance += chance
            avTowers[i][1].append(chance)
    cumChance = 0
    for tower in avTowers:
        for u in range(maxUpgrade):
            tower[1][u] /= totalChance + cumChance
            cumChance += tower[1][u]
            
    ## positions de depart (juste une, pour tout de suite)
    startPositions = []
    avBudget = totalBudget
    
    ## tourelles deja placees
    alreadyPlaced = []
    for placedTower in Game.level.towers.towers:
        alreadyPlaced.append(placedTower.type, placedTower.level,
            placedTower[0], placedTower.x, 0.75)
        avBudget -= TowerStats[placedTower.type][placedTower.level][TowerPRICE]
    startPositions.append([avBudget, alreadyPlaced])
    
    #####################
    ##  LOOP EVOLUTIF  ##
    #####################
    
    for progStep in range(progSteps):
        patience = nbTestPositions
        for n in range(nbTestPositions):
            
            ## on choisit une des positions de depart
            randPosNum = randint(0, len(startPositions)-1) \
                if len(startPositions) >= 2 else 0
            avBudget = startPositions[randPosNum][0]
            print 'Available Budget:', avBudget
            alreadyPlaced = startPositions[randPosNum][1]
            print '', alreadyPlaced
            
            ## on garde ou non des tourelles deja placees
            if rand() < propOfKeepingAll:
                nbToKeep = randint(0, len(alreadyPlaced)-1) \
                    if len(startPositions) >= 2 else 0
                while len(alreadyPlaced) > nbToKeep:
                    indToRemove = randint(0, len(alreadyPlaced)-1) \
                        if len(startPositions) >= 2 else 0
                    t, u = alreadyPlaced[indToRemove][0], alreadyPlaced[indToRemove][1]
                    chance = 1 - ((1 - TowerStats[t][u][12]) ** (5 * efficiencyInsistence))
                    if rand() > chance:
                        avBudget += TowerStats[t][u][TowerPRICE] \
                            * alreadyPlaced[indToRemove][4]
                        alreadyPlaced.pop(indToRemove)
            
            budgetLimit = avBudget*rand()
            
            T = [0 for i in range(TowerTYPES)]
            budgetSpent = 0
            while budgetSpent <= budgetLimit and patience and nbAvEmp:
                # on essaie d'ajouter une tourelle, preferant les plus efficaces
                towerChooser = 1.0*rand()
                t, u = -1, -1
                for tposs, uposs in iter(avTowers, maxUpgrade):
                    if towerChooser < tower[1][u]:
                        t, u = avTowers[tposs][0], uposs
                
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
        
        ## on garde les meilleures positions selon leur score
        nbKeptPositions = min(len(testPositions), 2*log(len(testPositions)))
        startPositions = []
        while len(startPositions) < (nbKeptPositions):
            bestScore = 0
            for position in testPositions:
                score = position[2]
                if score > bestScore:
                    bestScore = score
                    bestPosition = position
            startPositions.append(bestPosition)
            testPositions.remove(bestPosition)
    
    #########################
    ##  FIN LOOP EVOLUTIF  ##
    #########################
    
    ## on note la meilleure position
    bestScore = 0
    for position in testPositions:
        score = position[2]
        if score > bestScore:
            bestScore = score
            bestPosition = position
    
    ## on y fait correspondre le niveau
    # on max le budget
    Game.level.money = totalBudget
    # on efface les tourelles existantes
    Game.towers.clear()
    # on place les tourelles choisies
    for chosenTower in bestPosition[1]:
        Game.towers.placeTower(chosenTower[0], chosenTower[1],
            chosenTower[2], chosenTower[3])
    # on update le budget
    Game.level.money = bestPosition[0]
    
    
    # choisir et evaluer les tourelles selon les waves a venir aussi?
    # a condition que la wave actuelle reussisse!
    
    
    
    
    
    
    
    