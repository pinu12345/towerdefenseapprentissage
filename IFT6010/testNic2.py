# -*- coding: utf-8 -*-
from editDistance import *
from evalDistance import *
from random import *

txList = open('train.texto').readlines()
frList = open('train.fr').readlines()

num = 615
num = randint(0, len(txList))

print "\n\n"
print "--- Texto", num, "---"
print
tx = txList[num].rstrip()
fr = frList[num].rstrip()
#tx = "ZZZA B D E F"
#fr = "ARB C F"
print " tx: ", tx
print " fr: ", fr
print

affiche_normList(addNorms(tx, fr))

    
if 0:

    ## evalDistance

    tx = open('train.texto').readlines()
    fr = open('train.fr').readlines()
    num_tx = len(tx)
    #num_tx = 1100

    total_evalDistance = 0

    for n in range(num_tx):
        total_evalDistance += evalDistance(tx[n], fr[n])

    print
    print 100 * total_evalDistance // num_tx, "%"


    ## editDistance
    
    total_editDistance = 0

    for n in range(len(tx)):
        total_editDistance += editDistance(tx[n], fr[n])

    print
    print total_editDistance


    ## De P-O
    
    for line in open('normalisations.txt'):
        txt, trans = line.split()
        dictionary[txt] = trans

    #apply them to texto
    for line in texto:
        words =  re.findall(r"[^\s.,!?;]+|[.,!?;]", line)
        for word in words:
            if word in dictionary:
                norm.write(dictionary[word] + ' ')
            else:
                norm.write(str(word) + ' ')
        norm.write('\n')