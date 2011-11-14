 # coding=utf-8
import random
import math

def h(x):
    return math.sin(x) + 0.3 * x - 1

##Generation de Dn pour le numero 3 (Dn = generateDn(15))
def generateDn(n):
    random.seed(100)
    Dn = []
    Dn.append([])
    Dn.append([])
    for i in range(n):
        x = random.uniform(-5,5)
        Dn[0].append(x)
        Dn[1].append(h(x))
    return Dn