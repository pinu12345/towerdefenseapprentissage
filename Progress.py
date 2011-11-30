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
    maxFalsePositiveRisk = 0.01 # risque empirique qu'un negatif soit declare positif
    efficiencyInsistence = 5.0 # insistance vers les meilleures tourelles
    probOfKeepingAll = 0.5 # chance de garder toutes les tourelles deja en place
    
    targetVictoryChance = 1 - maxFalsePositiveRisk
    
    M = Game.level.map.M
    waves = Game.level.levelWaves
    curWave = Game.level.currentWave
    maxWave = Game.level.maxWave
    budgetList = Game.level.levelBudget
    
    initBudget = Game.level.money
    
    enemy = waves[curWave][0]
    number = waves[curWave][1]
    
    empVal = AemplacementValues(M)
    nbAvEmpInit = len(empVal)
    nbAvEmp = nbAvEmpInit
    avTowers = []
    for avTower in Game.level.levelTowers:
        avTowers.append([avTower])
        
    nbAvTowers = len(avTowers)
    maxUpgrade = Game.level.levelUpgrades
    nbPossiblePositions = (nbAvTowers * (maxUpgrade+1) + 1) ** nbAvEmp
    print '\n Number of possible positions:', nbPossiblePositions
    progSteps = int(1+log(nbPossiblePositions)/5) # nombre de generations
    # nbPP: facilement des millions
    #nbTestPositions = min(10, 100 * int((nbPossiblePositions)**.1))
    #nbTestPositions = max(100, 10 * int((nbPossiblePositions)**.1))
    nbTestPositions = 10 + progSteps
    print ' Number of spawned positions per generation:', nbTestPositions
    print ' Number of survivors per generation:', int((2*log(nbTestPositions))), '\n'
    
    testPositions = []
    #towerValues = zeros(6, 3)
    
    ## chances de base de choisir une tourelle
    totalChance = 0
    for i in ind(avTowers):
        avTowers[i].append([])
        for u in range(maxUpgrade+1):
            chance = 1.0 * TowerStats[avTowers[i][0]][u][12][enemy] \
                ** (efficiencyInsistence / progSteps)
            totalChance += chance
            avTowers[i][1].append(chance)
    cumChance = 0
    for tower in avTowers:
        for u in range(maxUpgrade+1):
            tower[1][u] = 1.0 * tower[1][u] / totalChance
            cumChance += tower[1][u]
            tower[1][u] = cumChance
    
    ## positions de depart (juste une, pour tout de suite)
    startPositions = []
    
    ## tourelles deja placees
    alreadyPlaced = []
    for placedTower in Game.level.towers.towers:
        #print '', placedTower.type, placedTower.level
        alreadyPlaced.append([placedTower.type, placedTower.level,
            placedTower.row, placedTower.column, 0.75])
    startPositions.append([initBudget, alreadyPlaced])
    #print '\n Max upgrade level:', maxUpgrade
    
    #####################
    ##  LOOP EVOLUTIF  ##
    #####################
    
    for progStep in range(progSteps):
        if progStep+1 < progSteps:
            print ' Generation', progStep+1, 'of', progSteps
        else:
            print ' Final generation'
        #print '\n\n --------------'
        #print '  GENERATION', progStep+1
        #print ' --------------'
        #print '\n Available start positions:'
        #for position in startPositions:
        #    print ' ', position
        #print
        patience = nbTestPositions
        for n in range(nbTestPositions):
            
            nbAvEmp = nbAvEmpInit
            
            ## on choisit une des positions de depart
            randPosNum = randint(0, len(startPositions)-1) \
                if len(startPositions) >= 2 else 0
            #print ' Start position chosen:', randPosNum
            avBudget = startPositions[randPosNum][0]
            #print ' Available Budget:', avBudget
            alreadyPlaced = []
            for elem in startPositions[randPosNum][1]:
                alreadyPlaced.append(elem)
            #if alreadyPlaced:
            #    print ' Towers already placed:'
            #    for tower in alreadyPlaced:
            #        print ' ', tower
            #else:
            #    print ' Towers already placed: none'
            
            ## on garde ou non des tourelles deja placees
            if alreadyPlaced and rand() > probOfKeepingAll:
                #print " Let's remove some of them towars!"
                nbToKeep = randint(0, len(alreadyPlaced)-1) \
                    if len(alreadyPlaced) >= 2 else 0
                while len(alreadyPlaced) > nbToKeep:
                    indToRemove = randint(0, len(alreadyPlaced)-1) \
                        if len(alreadyPlaced) >= 2 else 0
                    t, u = alreadyPlaced[indToRemove][0], alreadyPlaced[indToRemove][1]
                    chanceOfStaying = 1 - ((1 - TowerStats[t][u][12][enemy] \
                        * alreadyPlaced[indToRemove][4] ** 2) \
                        ** (10 * efficiencyInsistence / progSteps)) \
                        if len(alreadyPlaced) >= 2 else 0
                    #print " Should we remove tower number", indToRemove, "?"
                    #print "  Its chances of staying is", chanceOfStaying, "."
                    if rand() > chance:
                        #print "  It's removed!"
                        avBudget += calcTowerPrice(t, u) \
                            * alreadyPlaced[indToRemove][4]
                        #print '  New available budget:', avBudget
                        alreadyPlaced.pop(indToRemove)
            
            budgetLimit = avBudget*(1-rand()**2)
            #print ' Budget limit:', budgetLimit
            
            T = [0 for i in range(TowerTYPES)]
            budgetSpent = 0
            while budgetSpent <= budgetLimit and patience and nbAvEmp:
                ## on essaie d'ajouter une tourelle, preferant les plus efficaces
                towerChooser = 1.0*rand()
                #print ' Random tower chooser:', towerChooser
                t, u = -1, -1
                for tposs, uposs in iter(avTowers, maxUpgrade+1):
                    #print '', avTowers[tposs]
                    #print '', avTowers[tposs][1]
                    #print '', avTowers[tposs][1][uposs]
                    if towerChooser < avTowers[tposs][1][uposs] \
                        and t == -1 and u == -1:
                        t, u = avTowers[tposs][0], uposs
                        break
                #print ' Tower chosen:', t, u
                choiceMade = 0
                if t >= 0 and u >= 0:
                    # on verifie si cette option a un minimum de sens
                    for emp in empVal:
                        #print '  Emplacement value:', emp[2][t][u]
                        if emp[2][t][u]:
                            #print '  Valid placement found'
                            choiceMade = 1
                            break
                if choiceMade:
                    # ca devrait marcher, on prend en note
                    budgetSpent += calcTowerPrice(t, u)
                    T[t*3 + u] += 1 # ajoute a tourelles a essayer de placer
                    nbAvEmp -= 1
                else:
                    # ca a echoue, on perd patience et on recommence
                    patience -= 1
            if budgetSpent <= avBudget:
                # on place cette position le mieux possible
                testTowers = placeTowers(M, T, alreadyPlaced, 1)
                #print ' Final towers:', alreadyPlaced
                testPositions.append([avBudget-budgetSpent, testTowers,
                    posScore(eval(testTowers, 0), avBudget-budgetSpent, targetVictoryChance)])
                #print ' Budget spent:', budgetSpent, 'of', avBudget
            #print
        
        #if testPositions[-1] == []:
        #    testPositions.remove(testPositions[-1])
        
        ## on garde les meilleures positions selon leur score
        nbKeptPositions = 1 if progStep == progSteps-1 \
            else min(len(testPositions), int(2*log(len(testPositions))))
        startPositions = []
        while len(startPositions) < (nbKeptPositions):
            bestScore = 0
            bestPosition = 0
            for position in testPositions:
                if position != []:
                    #print ' Verifying position:', position
                    score = position[2]
                    if score > bestScore:
                        bestScore = score
                        bestPosition = position
            if bestPosition:
                startPositions.append(bestPosition)
                testPositions.remove(bestPosition)
            else:
                break
        testPositions = []
        #print ' Best positions of generation', ''.join([str(progStep+1), ':'])
        #for position in startPositions:
        #    print ' ', position
    
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
    #Game.level.money = totalBudget
    # on efface les tourelles existantes
    Game.level.towers.clear()
    # on place les tourelles choisies
    print '\n Surviving position:'
    for chosenTower in bestPosition[1]:
        print ' ', chosenTower
        Game.level.towers.placeTower(chosenTower[0], chosenTower[1],
            chosenTower[2], chosenTower[3])
    print ' Position score:', bestPosition[2]
    # on update le budget
    Game.level.money = bestPosition[0]
    
    
    # choisir et evaluer les tourelles selon les waves a venir aussi?
    # a condition que la wave actuelle reussisse!
    
    
    
    
    
    
    
    