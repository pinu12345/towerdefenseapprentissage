import EnemyData, TowerData, numpy

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
rangeCircle   = ( 255, 255, 255)
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

#Offsets
enemyOffsets = ((0,224), (32,224), (64,224), (96,224),
                (0,256), (32,256), (64,256), (96,192), (96,256))

towerOffsets = [[(0, 32), (32, 32), (64, 32), (96, 32)],
                [(0, 64), (32, 64), (64, 64), (96, 64)],
                [(0, 96), (32, 96), (64, 96), (96, 96)],
                [(0,128), (32,128), (64,128), (96,128)],
                [(0,160), (32,160), (64,160), (96,160)],
                [(0,192), ( 0,192), ( 0,192), ( 0,192)]]

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

## Tuiles de background
#   0              1              2                   3     4
# [ RouteWE[0..4], RouteNE[0..2], Emplacements[0..2], Base, Wasteland[0..9] ]
mapOffsets = [
    [(128,0),(128,64),(128,32),(128,128),(128,96)],
    [(160,0),(160,64),(160,32)],
    [(0,0),(32,0),(64,0)],
    [(96,0)],
    [(160,96),(128,160),(160,192),(128,192),(128,224),(128,256), \
        (160,128),(160,160),(160,224),(160,256)]]

## Ennemis
#   0       1       2        3         4         5      6       7      8
# [ Sold[], Moto[], Buggy[], Camion[], Humvee[], IFV[], Tank[], Eng[], MT[] ]
# -> [ NOM, VALEUR, VITESSE(p/t), SPREAD(p), DIMENSIONS(p), HPBAR(p) ]
EnemyStats = EnemyData.EnemyStatsFromExcel

EnemyNAME = 0
EnemyVALUE = 1
EnemySPEED = 2
EnemySPREAD = 3
EnemyDIM = 4
EnemyHPBAR = 5


## Tourelles
#   0            1         2          3          4        5
# [ Mitraille[], Sniper[], Grenade[], Mortier[], Canon[], Radio[] ]
# -> [ Niveau1[], Niveau2[], Niveau 3[] ]
#   -> [ NOM, NIVEAU, PRIX, PORTEE(p), DELAI(t), SPLASH(p), Degats[] ]
#     -> [ ContreEnnemi0, ContreEnnemi1, ..., ContreEnnemi8 ]
TowerStats = TowerData.TowerStatsFromExcel

TowerNAME = 0
TowerLEVEL = 1
TowerPRICE = 2
TowerRANGE = 3
TowerDELAY = 4
TowerSPLASH = 5
TowerDAMAGE = 6

TowerTYPES = len(TowerStats)*len(TowerStats[0]) # en pratique: 18
TowerPlaceImportance = numpy.zeros(TowerTYPES)
for i in range(TowerTYPES):
    t = i / 3
    l = i % 3
    TowerPlaceImportance[i] = (TowerStats[t][l][TowerRANGE]+1) \
        / numpy.log(TowerStats[t][l][TowerPRICE])
TowerPlaceOrder = []
for i in range(TowerTYPES):
    t = TowerPlaceImportance.argmin()
    TowerPlaceOrder.append(t)
    TowerPlaceImportance[t] = 1000000

DataSHOTS = 0
DataDAMAGE = 0


# [ ShotColor, ShotOffset, Width, ZoneColor1, ZoneColor2 ]
ShotGraphs = [
    [ (255, 255, 255), 5, 1, 0 ],
    [ (255, 255, 255), 7, 2, 0 ],
    [ (230, 230, 184), 4, 3, (255, 255, 255), (230, 230, 184) ],
    [ (230, 230, 184), 2, 6, (255, 255, 255), (230, 230, 184) ],
    [ (255, 255, 255), 7, 4, (255, 255, 255), (230, 230, 184) ],
    [ 0, 0, 0, (102, 255, 102), (42, 229, 42) ]
]

ShotCOLOR = 0
ShotOFFSET = 1
ShotWIDTH = 2
ShotZONECOLOR = 3
ShotZONEFARCOLOR = 4
    
# [ ShotColor, Dur, Width, ZoneColor, Dur ]
#ShotGraphs = \
#    [[ ( 255, 255, 180 ), 4,   2,     ( 0,   0,   0   ), 0  ],
#    [  ( 200, 210, 255 ), 20,  4,     ( 0,   0,   0   ), 0  ],
#    [  ( 0,   0,   0,  ), 0,   0,     ( 255, 100, 0   ), 1 ],
#    [  ( 220, 160, 20  ), 4,   8,     ( 200, 150, 0   ), 20 ],
#    [  ( 220, 160, 20  ), 4,   8,     ( 200, 150, 0   ), 20 ],
#    [  ( 255, 255, 255 ), 1,   3,     ( 255, 255, 255 ), 1  ]]