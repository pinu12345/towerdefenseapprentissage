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
        return sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)
    else:
        return sqrt((a-c)**2+(b-d)**2)

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

