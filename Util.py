from numpy import *
from Global import *
import Game

def mapToPixel(y, x = -1):
    # accepte nombre, deux nombres ou vecteurs de deux nombres
    if x < 0:
        if hasattr(y, "__getitem__"):
            return ([mapToPixel(y[0]), mapToPixel(y[1])])
        else:
            return y * tileSize
    else:
        return ([mapToPixel(y), mapToPixel(x)])

def pixelToMap(y, x = -1):
    # accepte nombre, deux nombres ou vecteurs de deux nombres
    if x < 0:
        if hasattr(y, "__getitem__"):
            return ([pixelToMap(y[0]), pixelToMap(y[1])])
        else:
            return y // tileSize
    else:
        return ([pixelToMap(y), pixelToMap(x)])
        
def distPixel(a, b, c = -1000, d = -1000, map = 0):
    # accepte a et b chacun vecteur [y, x]
    # ou a = y1, b = x1, c = y2, d = x2
    # input et output en pixels
    if c == -1000 or d == -1000:
        return sqrt((a[0]-b[0])**2+(a[1]-b[1])**2) - .1*tileSize
    else:
        return sqrt((a-c)**2+(b-d)**2) - 1

def distMap(a, b, c = -1000, d = -1000, map = 0):
    # accepte a et b chacun vecteur [y, x]
    # ou a = y1, b = x1, c = y2, d = x2
    # input et output en pixels
    if c == -1000 or d == -1000:
        return sqrt((a[0]-b[0])**2+(a[1]-b[1])**2) - .1*tileSize
    else:
        return sqrt((a-c)**2+(b-d)**2) - .1
        
def findEntrance(M):
    # N
    for x in range(1, mapWidth-1):
        if M[0][x] == car_path:
            return [[0, x], cardS]
    # S
    for x in range(1, mapWidth-1):
        if M[mapHeight-1][x] == car_path:
            return [[mapHeight-1, x], cardN]
    # W
    for y in range(1, mapHeight-1):
        if M[y][0] == car_path:
            return [[y, 0], cardE]
    # E
    for y in range(1, mapHeight-1):
        if M[y][mapWidth-1] == car_path:
            return [[y, mapWidth-1], cardW]

def emplacementValues(M):
    # renvoie une liste d'emplacements avec leurs coordonnees 
    #   et leur qualite pour chaque type et niveau de tourelle
    #   coordonnees: empVal[num_emp][0], empVal[num_emp][1]
    #   valeur d'emp: empVal[num_emp][2][tower_type][tower_level]
    ## approximatives pour l'instant, pas au pixel pres
    emplacements = []
    for y in range(mapHeight):
        for x in range(mapWidth):
            if M[y][x] == car_turret:
                cur_emp = [y, x, []]
                #py, px = mapToPixel(y), mapToPixel(x)
                for tower in range(len(TowerStats)):
                    cur_emp[2].append([])
                    for level in range(len(TowerStats[tower])):
                        cur_emp[2][tower].append([])
                        tower_range = TowerStats[tower][level][TowerRANGE]/tileSize
                        tower_splash = TowerStats[tower][level][TowerSPLASH]/tileSize
                        offset = max(tower_range, tower_splash)
                        tower_reach = 0
                        for ty in range(max(0, y-offset), \
                            min(mapHeight-1, y+offset+1)):
                            for tx in range(max(0, x-offset), \
                                min(mapWidth-1, x+offset+1)):
                                if M[ty][tx] == car_path:
                                    dM = distMap(x, y, tx, ty)
                                    if dM <= tower_range:
                                        tower_reach += 1
                                    elif dM <= tower_splash:
                                        tower_reach += (tower_splash-dM)/tower_splash
                        cur_emp[2][tower][level] = int(round(tower_reach))
                emplacements.append(cur_emp)
    return emplacements