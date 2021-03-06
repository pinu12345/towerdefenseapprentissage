﻿# -*- coding: utf-8 -*-
#from dictMaker import *
from dictTrad import *
from editDistance import *
from evalDistance import *
from bigramme import *
from trigramme import *
import string, types, numpy

txList = open('dev.texto').readlines()
txCopy = txList[:]
frList = open('dev.fr').readlines()

num_tx = 10
#num_tx = len(txList)

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
            result[i].append(wordsByDepth[j][k])
    return result

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
                    if trigramme[i][j][k][0] == w2:
                        if trigramme[i][j][k][1] == w1:
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

for i in range(num_tx):
    #txList[i] = wordSplit(txList[i])
    txCopy[i] = wordSplit(txCopy[i].lower())
    #frList[i] = wordSplit(frList[i])

al = 0.80
be = 0.13
ga = 0.06
la = 0.01

#Compte des trigrammes et bigrammes
countTrigramme = 0
for i in range(len(trigramme)):
    for j in range(len(trigramme[i])):
        if j != 0:
            for k in range(len(trigramme[i][j])):
                countTrigramme += trigramme[i][j][k][2]
print("Count trigramme : ", countTrigramme)     
    
for s in range(num_tx):
    # inserer une liste de candidats vide
    candidats = []
    #txCopy[s] : la phrase
    #print('======================')
    #print(txCopy[s])
    for w in range(len(txCopy[s])):
        word = txCopy[s][w]
        a = 0
        b = len(dict)
        word_found = 0
        while a != b:
            i = (a+b)/2
            if dict[i][0] == word:
                a = b
                word_found = 1
            elif dict[i][0] < word:
                a = i+1
            else:
                b = i
        if word_found:
            trads = dict[i][1]
            sum_candidats = 0
            for j in range(len(trads)):
                sum_candidats += trads[j][1]
            for j in range(len(trads)):
                if trads[j][1] > sum_candidats * 0.10:
                    #print('Adding : ' + trads[j][0])
                    candidats = addAll(candidats, trads[j][0], 2*w)
            txCopy[s][w] = trads[j][0]
        else:
            #print('WORD NOT FOUND : ' + word)
            candidats = addAll(candidats, word, 2*w)

           
    #print("")

    results = toList(candidats)
    maxProb = 0
    #print("===================")
    for i in range(len(results)):
        w2 = 'BOS'
        w1 = 'BOS'
        w0 = 'BOS'
        prob = 1
        #print("Norm : ", results[i]),
        for j in range(len(results[i])):
            w0 = results[i][j]
            #print(w2 + ', ' + w1 + ', ' + w0),
            tri = findTrigramme(w0, w2, w1)*al/countTrigramme
            bi  = findBigramme(w0, w1)*be/countTrigramme
            uni = findUnigramme(w0)*ga/countTrigramme
            zero = la/countTrigramme
            wprob = tri + bi + uni + zero
            #print wprob
            #Set w2 to w1 and w1 to w0
            w2 = w1
            w1 = w0
            prob *= wprob
        #print prob
        if prob > maxProb:
            maxProb = prob
            bestNorm = results[i]
        #print("")
    #print("BestNorm : ", bestNorm)
    ## ACCEPTÉ PAR LE MODELE DE LANGUE
    txCopy[s] = bestNorm
    
    ## Traduction terminee, passons aux regles specifiques
    for k in range(len(txCopy[s])):
        if txCopy[s][k] in ['florent', 'claude', 'virginie', 'amélie']:
            txCopy[s][k] = txCopy[s][k].capitalize()
    txCopy[s] = ' '.join(txCopy[s])
    txCopy[s] = txCopy[s][0].capitalize() + txCopy[s][1:]
    txCopy[s] = string.replace(txCopy[s], " ' ", "'")
    txCopy[s] = string.replace(txCopy[s], " ,", ",")
    txCopy[s] = string.replace(txCopy[s], " - ", "-")
    txCopy[s] = string.replace(txCopy[s], " .", ".")
    txCopy[s] = string.replace(txCopy[s], " !", "!")
    txCopy[s] = string.replace(txCopy[s], " ?", "?")
    txCopy[s] = string.replace(txCopy[s], " j ", " j'")
    txCopy[s] = string.replace(txCopy[s], "J ", "J'")
    txCopy[s] = string.replace(txCopy[s], " t ", " t'")
    txCopy[s] = string.replace(txCopy[s], "T ", "T'")
    txCopy[s] = string.replace(txCopy[s], " m ", " m'")
    txCopy[s] = string.replace(txCopy[s], "M ", "M'")
    txCopy[s] = string.replace(txCopy[s], " n ", " n'")
    txCopy[s] = string.replace(txCopy[s], "N ", "N'")
    txCopy[s] = string.replace(txCopy[s], " l ", " l'")
    txCopy[s] = string.replace(txCopy[s], "L ", "L'")
    txCopy[s] = string.replace(txCopy[s], " qu ", " qu'")
    txCopy[s] = string.replace(txCopy[s], "Qu ", "Qu'")
    if txCopy[s][len(txCopy[s])-1] not in ['.', '!', '?', ')', '(']:
        if txCopy[s][len(txCopy[s])-2] == ':':
            if len(txCopy[s]) > 2:
                if txCopy[s][len(txCopy[s])-4] not in ['.', '!', '?']:
                    txCopy[s] = txCopy[s][:-3] + '.' + txCopy[s][-3:]
        elif txCopy[s][len(txCopy[s])-3] == ':':
            if len(txCopy[s]) > 3:
                if txCopy[s][len(txCopy[s])-5] not in ['.', '!', '?']:
                    txCopy[s] = txCopy[s][:-4] + '.' + txCopy[s][-4:]
        elif txCopy[s][len(txCopy[s])-1] != '-':
            txCopy[s] += '.'
    print txCopy[s]
    
print
for i in range(num_tx):
    txList[i] = ''.join(txList[i])
    print '', txList[i],
    print '', txCopy[i]
    frList[i] = ''.join(frList[i])
    print '', frList[i],
    print
    #pass
    
print ' ', round(100*evalTotalDistance(txList[:num_tx], frList[:num_tx]), 2), '%'
print '', round(100*evalTotalDistance(txCopy[:num_tx], frList[:num_tx]), 2), '%'

#str = '"lol'
#print str.replace('"', '\\"')
#print string.replace(str, '"', '\\"')
#print wordSplit('après')

#makeDict('train.texto', 'train.fr')
#for line in dict:
#    print '', line[0], '', line[1]