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
        return sqrt((a[0]-b[0])**2+(a[1]-b[1])**2) - .5
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

def precisePathMap(M):
    P = [[car_empty]*mapWidth*tileSize for i in range(mapHeight*tileSize)]
    #print '\n\n'
    #print mapHeight, mapWidth
    #print len(P), len(P[0])
    vcars = [car_path, car_base]
    for i in range(len(P)):
        for j in range(len(P[0])):
            # le point precis est-il au milieu d'une case?
            isq, jsq = not i % tileSize, not j % tileSize
            iM, jM = pixelToMap(i), pixelToMap(j)
            curp = M[iM][jM]
            if isq and jsq:
                if curp in vcars:
                    P[i][j] = car_path
            elif isq:
                if jM+1 < mapWidth:
                    nexp = M[iM][jM+1]
                else:
                    nexp = curp
                if curp in vcars and nexp in vcars:
                    P[i][j] = car_path
            elif jsq:
                if iM+1 < mapHeight:
                    nexp = M[iM+1][jM]
                else:
                    nexp = curp
                if curp in vcars and nexp in vcars:
                    P[i][j] = car_path
    return P

def emplacementList(M):
    # renvoie une liste d'emplacements avec leurs coordonnees 
    emplacements = []
    for y in range(mapHeight):
        for x in range(mapWidth):
            if M[y][x] == car_turret:
                emplacements.append([y, x])
    return emplacements
                
    
def emplacementProximities(M):
    # renvoie une liste d'emplacements avec leurs coordonnees 
    #   et leur proximite au chemin
    #   coordonnees: empVal[num_emp][0], empVal[num_emp][1]
    #   proximite: empVal[num_emp][2]
    emplacements = []
    for y in range(mapHeight):
        for x in range(mapWidth):
            if M[y][x] == car_turret:
                cur_emp = [y, x]
                #py, px = mapToPixel(y), mapToPixel(x)
                cur_emp.append(singleEmpValue(P, y, x))
                emplacements.append(cur_emp)
    return emplacements

def emplacementValues(M, P):
    # renvoie une liste d'emplacements avec leurs coordonnees 
    #   et leur qualite pour chaque type et niveau de tourelle
    #   coordonnees: empVal[num_emp][0], empVal[num_emp][1]
    #   valeur d'emp: empVal[num_emp][2][tower_type][tower_level]
    ## approximatives pour l'instant, pas au pixel pres
    emplacements = emplacementList(M)
    for emp in emplacements:
        y, x = emp[0], emp[1]
        if M[y][x] == car_turret:
            emp.append(singleEmpValue(P, y, x))
    return emplacements
    
def singleEmpValue(P, y, x):
    empTV = []
    for tower in range(len(TowerStats)):
        empTV.append([])
        for level in range(len(TowerStats[tower])):
            empTV[tower].append([])
            tower_reach = singleTowerEmpValue(P, y, x, tower, level)
            empTV[tower][level] = int(round(tower_reach))
    return empTV
    
def singleTowerEmpValue(P, y, x, tower, level):
    y, x = mapToPixel(y), mapToPixel(x)
    tower_range = TowerStats[tower][level][TowerRANGE]
    tower_splash = TowerStats[tower][level][TowerSPLASH]
    offset = max(tower_range, tower_splash)
    tower_reach = 0
    for ty in range(max(0, y-offset), \
        min(mapHeight*tileSize-1, y+offset+1)):
        for tx in range(max(0, x-offset), \
            min(mapWidth*tileSize-1, x+offset+1)):
            if P[ty][tx] == car_path:
                dM = distPixel(x, y, tx, ty)
                if dM <= tower_range:
                    tower_reach += 1
                elif dM <= tower_splash:
                    tower_reach += (tower_splash-dM)/tower_splash
    return tower_reach