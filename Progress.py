import os, Game
from Global import *
from math import *
from numpy import *
from Util import *
from DataTreatment import *
from Evaluate import *


def prog(placedTowers = Game.level.towers):
    ## une des trois fonctions majeures
    # utilise l'info dans Game.level et Global
    # pour progresser vers une position optimale
    M = Game.level.map.M
    waves = Game.level.waves
    curWave = Game.level.currentWave
    maxWave = Game.level.maxWaves
    budget = ...
    
    enemy = waves[curWave][0]
    number = waves[curWave][1]
    
    empVal = AemplacementValues(M)
    nbAvEmp = len(empVal)
    avTowers = [0, 1, 2, 3, 4, 5] # a changer
    nbAvTowers = len(avTowers)
    maxUpgrade = 2 # a changer
    nbPossiblePositions = (nbAvTowers * (maxUpgrade+1) + 1) ** nbAvEmp
    # nbPP: facilement des millions
    nbTestPositions = 5 * int(nbPossiblePositions**.25)
    testPositions = []
    #towerValues = zeros(6, 3)
    
    ## tourelles deja placees
    alreadyPlaced = []
    for placedTower in Game.level.towers:
        alreadyPlaced.append(placedTower.type, placedTower.level,
            placedTower.y, placedTower.x)
    
    ## chances de base de choisir une tourelle
    totalChance = 0
    efficiencyInsistence = 1 # hyperparametre: 1 a la base
    for tower in avTowers:
        tower.append([])
        for u in range(maxUpgrade):
            chance = TowerStats[tower][u][12] ** efficiencyInsistence
            totalChance += chance
            tower[1].append(chance)
    cumChance = 0
    for tower in avTowers:
        for u in range(maxUpgrade):
            tower[1][u] /= totalChances + cumChance
            cumChance += tower[1][u]
    
    ## on garde ou non des tourelles deja en place
    if random() < 0.5:
        
    
    ## generation de positions possibles
    patience = nbTestPositions
    for n in range(nbTestPositions):
        budgetSpent = 0
        budgetLimit = budget*random()
        T = [0 for i in range(TowerTYPES)]
        while budgetSpent <= budgetLimit and patience and nbAvEmp:
            # on essaie d'ajouter une tourelle, preferant les plus efficaces
            towerChooser = 1.0*random()
            t, u = -1, -1
            for tposs, uposs in iter(avTowers, maxUpgrade):
                if towerChooser < tower[1][u]:
                    t, u = avTowers[tposs][0], uposs
            if t >= 0 and u >= 0:
                # on verifie si cette option a un minimum de sens
                choiceMade = 0
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
        # on place cette position le mieux possible
        testTowers = placeTowers(M, T, alreadyPlaced, 1)
        testPositions.append([])
        testPositions[n][0] = testTowers
        testPositions[n][1] = eval(testTowers)
    
    ## on garde les meilleures solutions
    # on choisit comment?
    
    nbKeptSolutions = max(len(testPositions), 2*log(nbTestPositions))
    bestSolutions = []
    while len(bestSolutions) < (nbKeptSolutions):
        best
        for
        
            
    # choisir et evaluer les tourelles selon les waves a venir aussi?
    # a condition que la wave actuelle reussisse!
    
    
    
    
    
    
    
    