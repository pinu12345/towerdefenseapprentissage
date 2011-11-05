# Tower States
NORMAL = 0
SHOOTNORMAL = 1
DIAGONAL = 2
SHOOTDIAGONAL = 3

# etats
STATE_INITMENU = 0
STATE_MENU = 1
STATE_PREPARATION = 2
STATE_GAME = 3
STATE_INITGAMEMENU = 4
STATE_GAMEMENU = 5
STATE_LOADGAME = 6

# couleurs
background    = (   0,   0,   0)
rangeCircle   = (  20, 100,  20, 10)
pink          = ( 255,   0, 255)
spritepink    = ( 255, 127, 255)

# dimensions de carte
mapWidth = 24
mapHeight = 16
showGrid = 0
tileSize = 32
gridSize = 1

rightMenuSize = 200
bottomMenuSize = 100

# carte .txt: caracteres vide, chemin, emplacement et base
car_empty  = '-'
car_path   = 'X'
car_turret = 'O'
car_base   = 'B'

# Points cardinaux
cardN, cardS, cardW, cardE, cardNW, cardNE, cardSW, cardSE = 0, 1, 2, 3, 4, 5, 6, 7

## Enemy Types
EnemyNAME = 0
EnemyVALUE = 1
EnemyHP = 2
EnemyARMOR = 3
EnemySPEED = 4
EnemyDELAY = 5

#Offsets
enemyOffsets = ((0,224), (32,224),(64,224),(96,224),
                (0,256), (32,256),(64,256),(96,256))

towerOffsets = [[(0, 32), (32, 32), (64, 32), (96, 32)],
                [(0, 64), (32, 64), (64, 64), (96, 64)],
                [(0, 96), (32, 96), (64, 96), (96, 96)],
                [(0,128), (32,128), (64,128), (96,128)],
                [(0,192)],
                [(0,160), (32,160), (64,160), (96,160)]]

MAPROUTE = 0
MAPROUTTURN = 1
MAPEMPLACEMENT = 2
MAPBASE = 3
MAPWASTELAND = 4

ROUTEH  = 0
ROUTEV  = 1
ROUTENW = 2
ROUTENE = 3
ROUTESE = 4
ROUTESW = 5
BASEN = 6
BASES = 7
BASEE = 8
BASEW = 9
EMPLACEMENT = 10
WASTELAND = 11

mapOffsets = [[(128,0),(128,32),(128,64),(128,96),(128,128)],
              [(160,0),(160,32),(160,64)],
              [(0,0),(32,0),(64,0)],
              [(96,0)],
              [(160,96),(128,160),(128,192),(128,224),(128,256),(160,128),(160,160),(160,192),(160,224),(160,256)]]

## Name             Value   HP      Armor   Speed   Delay
EnemyTypes = \
    [["Ninja",      5,      100,    0,      100,   48],
    ["Pirate",      5,      200,    0,      60,    48],
    ["Singe",       1,      50,     0,      80,    32],
    ["BebeDino",    15,     500,    5,      50,    64],
    ["Dinosaure",   40,     1000,   10,     40,    128]]
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
    [["Mitraille",  [100, 210, 300],
                    [  2,   5,   10],
                    [  32,   10,   8],
                    [  5,   6,   7],
                    [  0,   0,   0]],
    ["Sniper",      [200],
                    [80],
                    [100],
                    [10],
                    [0]],
    ["Zone",        [100],
                    [4],
                    [20],
                    [0],
                    [2]],
    ["Omega",       [500],
                    [100],
                    [100],
                    [12],
                    [3]],
    ["Omega2",      [500],
                    [100],
                    [100],
                    [12],
                    [3]],
    ["Hax",         [1, 1, 1, 1],
                    [1000, 1500, 2000, 3000],
                    [1, 1, 1, 1],
                    [4, 4, 3, 3],
                    [1, 1, 1, 1]]]

##     Shot Color         Dur  Width  Zone Color         Dur
TowerShotGraphs = \
    [[ ( 255, 255, 180 ), 4,   2,     ( 0,   0,   0   ), 0  ],
    [  ( 200, 210, 255 ), 20,  4,     ( 0,   0,   0   ), 0  ],
    [  ( 0,   0,   0,  ), 0,   0,     ( 255, 100, 0   ), 1 ],
    [  ( 220, 160, 20  ), 4,   8,     ( 200, 150, 0   ), 20 ],
    [  ( 220, 160, 20  ), 4,   8,     ( 200, 150, 0   ), 20 ],
    [  ( 255, 255, 255 ), 1,   3,     ( 255, 255, 255 ), 1  ]]