# -*- coding: utf-8 -*-
import types
import json
import numpy
from bigramme import *
from trigramme import *

def depth(list):
    if list == []:
        return 1
    cur = list[:]
    max = 0
    for i in range(len(list)):
        if type(list[i]) is types.ListType :
            temp = depth(list[i])
            if max < temp:
                max = temp
    return 1 + max

def addAll(list, item, level):
    if list == []:
        list = [[item,[]]]
    elif level == 0:
        list.append([item,[]])
    else:
        for i in range(len(list)):
            list[i][1] = addAll(list[i][1], item, level-2)
    return list

def toList(list):
    listdepth = depth(list)/2
    current = list[:]
    counts = [len(current)]
    size = counts[0]
    wordsByDepth = []
    for i in range(listdepth):
        wordsByDepth.append([])
        for j in range(counts[i]):
            wordsByDepth[i].append(current[j][0])
        if i == listdepth-1:
            break
        current = current[0][1]
        counts.append(len(current))
        size *= counts[i+1]
    modulos = numpy.ones(len(counts))    
    for i in range(len(counts)-1, 0, -1):
        modulos[:i] *= counts[i]
    result = []
    for i in range(size):
        result.append([])
        for j in range(listdepth):
            k = (i/int(modulos[j]))%counts[j]
            result[i].append([wordsByDepth[j][k]])
            
def findTrigramme(w0, w2, w1):
    found = 0
    for i in range(len(trigramme)):
        for j in range(len(trigramme[i])):
            if j == 0 and trigramme[i][j] == w0:
                found = 1
            if j != 0:
                if found == 0 :
                    continue
                for k in range(len(trigramme[i][j])):
                    if trigramme[i][j][k][0] == w2 and trigramme[i][j][k][1] == w1:
                        return trigramme[i][j][k][2]
    return 0
    
def findBigramme(w0, w1):
    found = 0
    for i in range(len(bigramme)):
        for j in range(len(bigramme[i])):
            if j == 0 and bigramme[i][j] == w0:
                found = 1
            if j != 0:
                if found == 0 :
                    continue
                for k in range(len(bigramme[i][j])):
                    if bigramme[i][j][k][0] == w1:
                        return bigramme[i][j][k][1]
    return 0

def findUnigramme(w0):
    found = 0
    for i in range(len(trigramme)):
        for j in range(len(trigramme[i])):
            if j == 0 and trigramme[i][j] == w0:
                found = 1
            if found == 0 :
                continue
            if j != 0:
                sum = 0
                for k in range(len(trigramme[i][j])):
                    sum += trigramme[i][j][k][2]
                return sum
    return 0

print findBigramme('Donne', "BOS")
print findBigramme('Dubois', "Claude")
print findBigramme('Effectivement', "BOS")
