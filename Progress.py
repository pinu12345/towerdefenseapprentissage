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
    
    empVal = AemplacementValues(M)
    avTowers = [0, 1, 2, 3, 4, 5]
    nbAvTowers = len(possibleTowers)6 # a changer
    maxUpgrade = 2
    nbPossiblePositions = (nbAvTowers * (maxUpgrade+1) + 1) ** len(empVal)
    # nbPP: facilement des millions
    nbTestPositions = 5 * int(nbPossiblePositions**.25)
    testPositions = []
    placedTowers = []
    towerValues = zeros(6, 3)
    for tower in avTowers:
        for u in range(maxUpgrade):
            
    for n in range(nbTestPositions):
        
        # garder ou non les tourelles deja en place
    
    # choisir et evaluer les tourelles selon les waves a venir aussi?
    # a condition que la wave actuelle reussisse!