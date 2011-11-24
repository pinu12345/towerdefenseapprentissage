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
    avTowers = [0, 1, 2, 3, 4, 5]
    nbAvTowers = len(possibleTowers)6 # a changer
    maxUpgrade = 2
    nbPossiblePositions = (nbAvTowers * (maxUpgrade+1) + 1) ** nbAvEmp
    # nbPP: facilement des millions
    nbTestPositions = 5 * int(nbPossiblePositions**.25)
    testPositions = []
    placedTowers = []
    #towerValues = zeros(6, 3)
    
    ## chances de base de choisir une tourelle
    totalChances = 0
    efficiencyInsistence = 1 # hyperparametre
    for tower in avTowers:
        tower.append([])
        for u in range(maxUpgrade):
            chances = TowerStats[tower][u][12] ** efficiencyInsistence
            totalChances += chances
            tower[1].append(chances)
    for tower in avTowers:
        for u in range(maxUpgrade):
            tower[1][u] /= totalChances
    
    ## on garde ou non les tourelles deja en place
    pass
    
    ## generation de positions possibles
    for n in range(nbTestPositions):
        budgetSpent = 0
        budgetLimit = budget*random()
        while budgetSpent <= budgetLimit:
            # on essaie d'ajouter une tourelle, preferant les plus efficaces
            
            # si pas d'emplacements: break
            
    # choisir et evaluer les tourelles selon les waves a venir aussi?
    # a condition que la wave actuelle reussisse!