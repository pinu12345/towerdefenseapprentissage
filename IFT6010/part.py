# -*- coding: utf-8 -*-
#from dictMaker import *
from dictTrad import *
from editDistance import *
from evalDistance import *
import string

txList = open('dev.texto').readlines()
txCopy = txList[:]
frList = open('dev.fr').readlines()

num_tx = 50
num_tx = len(txList)

for i in range(num_tx):
    #txList[i] = wordSplit(txList[i])
    txCopy[i] = wordSplit(txCopy[i].lower())
    #frList[i] = wordSplit(frList[i])

for s in range(num_tx):
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
            num_seen = 0
            for j in range(len(trads)):
                if trads[j][1] > num_seen:
                    num_seen = trads[j][1]
                    most_seen = j
            #print txCopy[s][w]
            txCopy[s][w] = trads[most_seen][0]
            #print txCopy[s][w]
            #print

    ## Traduction terminee, passons aux regles specifiques
    txCopy[s] = ' '.join(txCopy[s])
    txCopy[s] = txCopy[s].capitalize()
    txCopy[s] = string.replace(txCopy[s], " ' ", "'")
    txCopy[s] = string.replace(txCopy[s], " ,", ",")
    txCopy[s] = string.replace(txCopy[s], " - ", "-")
    txCopy[s] = string.replace(txCopy[s], " .", ".")
    txCopy[s] = string.replace(txCopy[s], " !", "!")
    txCopy[s] = string.replace(txCopy[s], " ?", "?")
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
    
print
for i in range(num_tx):
    #txList[i] = ' '.join(txList[i])
    print '', txList[i],
    print '', txCopy[i]
    #frList[i] = ' '.join(frList[i])
    print '', frList[i],
    print
    pass
    
print ' ', round(100*evalTotalDistance(txList[:num_tx], frList[:num_tx]), 2), '%'
print '', round(100*evalTotalDistance(txCopy[:num_tx], frList[:num_tx]), 2), '%'

#str = '"lol'
#print str.replace('"', '\\"')
#print string.replace(str, '"', '\\"')
#print wordSplit('après')

#makeDict('train.texto', 'train.fr')
#for line in dict:
#    print '', line[0], '', line[1]