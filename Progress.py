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
    placedTowers = []
    #towerValues = zeros(6, 3)
    
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
    pass
    
    ## generation de positions possibles
    patience = nbTestPositions
    for n in range(nbTestPositions):
        budgetSpent = 0
        budgetLimit = budget*random()
        testTowers = []
        while budgetSpent <= budgetLimit and patience and nbAvEmp:
            # on essaie d'ajouter une tourelle, preferant les plus efficaces
            towerChooser = 1.0*random()
            t, u = -1, -1
            for tposs, uposs in iter(avTowers, maxUpgrade):
                if towerChooser < tower[1][u]:
                    t, u = avTowers[tposs][0], uposs
            if t >= 0 and u >= 0:
                # on verifie si cette option a du sens
                choiceMade = 0
                towerRange = max(
                    TowerStats[t][u][TowerRANGE], TowerStats[t][u][TowerSPLASH])
                towerCost = 
                for emp in empVal:
                    if emp[2][t][u] and:
                        choiceMade = 1
                        break
            if choiceMade:
                # ca devrait marcher, on prend en note
                budgetSpent +=
                testTowers.append([t, u])
                nbAvEmp -= 1
            else:
                # ca a echoue, on perd patience et on recommence
                patience -= 1
            # si pas d'emplacements: break
            
    # choisir et evaluer les tourelles selon les waves a venir aussi?
    # a condition que la wave actuelle reussisse!