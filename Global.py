# couleurs
background    = (   0,   0,   0)
empty         = ( 120,  80,  40)
route         = ( 200, 190, 170)
tower         = ( 130, 140, 160)
base          = ( 200,  80,  20)
rangeCircle   = (  20, 100,  20, 10)

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
    [["Ninja",      5,      100,    0,      100,   100],
    ["Pirate",      5,      200,    0,      60,    100],
    ["Singe",       1,      50,     0,      80,    50],
    ["BebeDino",    15,     500,    5,      50,    200],
    ["Dinosaure",   40,     1000,   10,     40,    500]]
#                                       max 100
    
## Tower Types
TowerNAME = 0
TowerVALUE = 1
TowerDAMAGE = 2
TowerDELAY = 3
TowerRANGE = 4
TowerSPLASH = 5

## Nom              Value   Damage  Delay   Range   Splash
TowerTypes = \
    [["Mitraille",  100,    2,      5,      5,      0],
    ["Sniper",      200,    80,     100,    10,     0],
    ["Zone",        100,    4,      20,     0,      2],
    ["Omega",       500,    200,    100,    12,     3],
    ["Hax",         1,      1000,   1,      4,      1]]
    
##     Shot Color         Dur  Width  Zone Color         Dur
TowerShotGraphs = \
    [[ ( 255, 255, 180, 1 ), 4,   2,     ( 0,   0,   0   ), 0  ],
    [  ( 200, 210, 255, 20 ), 20,  4,     ( 0,   0,   0   ), 0  ],
    [  ( 0,   0,   0, 50   ), 0,   0,     ( 255, 100, 0, 50   ), 10 ],
    [  ( 220, 160, 20, 80  ), 4,   8,    ( 200, 150, 0   ), 20 ],
    [  ( 255, 255, 255, 255 ), 1,   3,     ( 0,   0,   0   ), 0  ]]