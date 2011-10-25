# couleurs
background    = (   0,   0,   0)
empty         = ( 120,  80,  40)
route         = ( 200, 190, 170)
tower         = ( 130, 140, 160)
base          = ( 200,  80,  20)

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
    [["Ninja",      5,      1000,   0,      100,    16],
    ["Pirate",      5,      2000,   0,      100,    32],
    ["Singe",       1,      1500,   0,      100,    8],
    ["BebeDino",    1,      2000,   5,      100,    32],
    ["BebeDino",    1,      2000,   20,     100,    32],
    ["BebeDino",    1,      2000,   5,      100,    32],
    ["Dinosaure",   40,     1000,   10,     100,    32]]
    
## Tower Types
TowerNAME = 0
TowerVALUE = 1
TowerDAMAGE = 2
TowerDELAY = 3
TowerRANGE = 4
TowerSPLASH = 5

## Nom              Value   Damage  Delay   Range   Splash
TowerTypes = \
    [["Mitraille",  100,    5,      0.1,    5,      0],
    ["Sniper",      200,    20,     4,      10,     0],
    ["Zone",        100,    20,     1,      0,      2],
    ["Omega",       500,    200,    2,      3,      1],
    ["Hax",         1,      1000,   0.1,    2,      5]]
    
##     Shot Color         Dur  Width  Zone Color         Dur
TowerShotGraphs = \
    [[ ( 255, 255, 180 ), 4,   2,     ( 0,   0,   0   ), 0  ],
    [  ( 200, 210, 255 ), 20,  4,     ( 0,   0,   0   ), 0  ],
    [  ( 0,   0,   0   ), 0,   0,     ( 255, 100, 0   ), 10 ],
    [  ( 255, 240, 200 ), 4,   1,     ( 255, 200, 100 ), 20 ],
    [  ( 255, 255, 255 ), 1,   3,     ( 0,   0,   0   ), 0  ]]