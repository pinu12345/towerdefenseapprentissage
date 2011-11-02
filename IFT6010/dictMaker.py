# -*- coding: utf-8 -*-
import re, operator, time
from editDistance import *

txList = open('train.texto').readlines()
frList = open('train.fr').readlines()
#norm = open('train.norm', 'w')
dict = []

#for num_tx in [len(txList)]:
for num_tx in [len(txList)/100]:
#for num_tx in [10, 40, 100, 400, 1000, 4000, 10000]:
    start_time = time.clock()
    num_tx = min(num_tx, len(txList))
    for i in range(num_tx):
        #print "\n--- Texto", i+1 , "---\n"
        tx, fr = txList[i], frList[i]
        wordPairs = addNorms(tx, fr)
        #affiche_normList(wordPairs)
        for j in range(len(wordPairs)):
            txWord, frWord = wordPairs[j][0], wordPairs[j][1]
            if txWord != frWord:
                # cherche txWord dans dict
                # ameliorable par recherche binaire
                txWordNotFound = 1
                for line in dict:
                    if txWord == line[0]:
                        txWordNotFound = 0
                        txWordLine = line
                        break
                if txWordNotFound:
                    # ajoute txWord au dict, puis ordonne
                    # ameliorable par insertion precise
                    dict.append([txWord, [[frWord, 1]]])
                    dict.sort()
                else:
                    # verifie si frWord existe deja
                    frWordNotFound = 1
                    for frTrad in txWordLine[1]:
                        if frWord == frTrad[0]:
                            frTrad[1] += 1
                            frWordNotFound = 0
                            break
                    if frWordNotFound:
                        txWordLine[1].append([frWord, 1])
    
    #print '\n Text:', num_tx
    #print ' Dict:', len(dict)
    #print ' Taux:', int(10000*len(dict)/num_tx)/100, '%'
    #end_time = time.clock()
    #delta_time = end_time - start_time
    #print ' Time:', int(delta_time)

for line in dict:
    print line[0], line[1]

    
def original_de_PO():
    #load the normalisations
    #for line in open('normalisations.txt'):
        #txt, trans = line.split()
        #dictionary[txt] = trans

    #apply them to texto
    for i in range(len(txList)):
        words =  re.findall(r"[a-zA-Z0-9àâæçéèêëîïôœùûüÿÀÂÆÇÉÈÊËÎÏÔŒÙÜŸ]+|[^\sa-zA-Z0-9àâæçéèêëîïôœùûüÿÀÂÆÇÉÈÊËÎÏÔŒÙÜŸ]+", line)
        for word in words:
            if word in dictionary:
                #norm.write(dictionary[word] + '\n')
                dictionary[word] += 1
            else:
                #norm.write(str(word) + '\n')
                dictionary[word] = 1

    sorted_dict = sorted(dictionary.iteritems(), key=operator.itemgetter(1), reverse = True)
    for line in sorted_dict:
        norm.write(str(line[1]) + ' ' + line[0] + '\n')