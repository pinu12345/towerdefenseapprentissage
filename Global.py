# dimensions de carte
mapWidth = 24
mapHeight = 16
showGrid = 0
tileSize = 32
gridSize = 1

# carte .txt: caracteres vide, chemin, emplacement et base
car_empty  = '-'
car_path   = 'X'
car_turret = 'O'
car_base   = 'B'

# Points cardinaux
cardN, cardS, cardW, cardE = 0, 1, 2, 3

## Enemy Types
EnemyNAME = 0
EnemyVALUE = 1
EnemyHP = 2
EnemyARMOR = 3
EnemySPEED = 4
EnemyDELAY = 5

## Name             Value   HP      Armor   Speed   Delay
EnemyTypes = \
    [["Ninja",      5,      100,    0,      10,      10],
    ["Pirate",      5,      200,    0,      10,      5],
    ["Singe",       1,      50,     0,      10,     5],
    ["BebeDino",    1,      200,    5,      10,      5],
    ["Dinosaure",   40,     1000,   10,     10,      5]]
    
## Tower Types
TowerNAME = 0
TowerVALUE = 1
TowerDAMAGE = 2
TowerDELAY = 3
TowerRANGE = 4
TowerSPLASH = 5

## Nom              Value   Damage  Delay   Range   Splash
TowerTypes = \
    [["Mitraille",  100,    2,      0.1,    4,      0],
    ["Sniper",      200,    200,    4,      10,     0],
    ["Zone",        100,    20,     1,      0,      2],
    ["Omega",       500,    200,    2,      12,     1],
    ["Hax",         1,      1000,   0.1,    100,    5]]