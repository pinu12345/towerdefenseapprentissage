 # coding=utf-8
import random
import math
import numpy

def h(x):
    return math.sin(x) + 0.3 * x - 1

##Generation de Dn pour le numero 3 (Dn = generateDn(15))
def generateDn(n):
    random.seed(100)
    Dn = numpy.zeros([n,2])
    for i in range(n):
        x = random.uniform(-5,5)
        Dn[i,0] = x
        Dn[i,1] = h(x)
    return Dn


