# -*- coding: utf-8 -*-
import re, operator, time, json, io, string
from editDistance import *
from dictTrad import *

def makeDict(docTx, docFr):
    txList = open('train.texto').readlines()
    frList = open('train.fr').readlines()
    #if 'dict' not in globals():
    dict = []
    #print dict[0][0]
    for num_tx in [len(txList)]:
    #for num_tx in [len(txList)/1000]:
    #for num_tx in [10, 40, 100, 400, 1000, 4000, 10000]:
    #for num_tx in [100]:
        start_time = time.clock()
        num_tx = min(num_tx, len(txList))
        for i in range(num_tx):
            #print "\n--- Texto", i+1 , "---\n"
            tx, fr = txList[i], frList[i]
            wordPairs = addNorms(tx, fr)
            #affiche_normList(wordPairs)
            for j in range(len(wordPairs)):
                txWord, frWord = wordPairs[j][0], wordPairs[j][1]
                #if txWord != frWord:
                if 1:
                    #print(txWord, frWord)
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
        
    dictDoc = open('dictTrad.py', 'w')
    dictDoc.write('# -*- coding: utf-8 -*-\ndict = ')
    #json.dump(dict, dictDoc)

    for i in range(len(dict)):
        if i == 0:
            dictDoc.write('[')
        dictDoc.write('["' + dict[i][0].replace('"', '\\"') + '", [')
        for j in range(len(dict[i][1])):
            dictDoc.write('["' + dict[i][1][j][0].replace('"', '\\"') + '", ' + str(dict[i][1][j][1]) + ']')
            if j != len(dict[i][1])-1:
                dictDoc.write(', ')
            else:
                dictDoc.write(']')
        dictDoc.write(']')
        if i != len(dict)-1:
            dictDoc.write(', \n')
        else:
            dictDoc.write(']')
            
        #print 'line 0 :', line[0]
        #print 'line 1 :', line[1][0][0]
        #for word in line[1]
            #print '-->', wo1rd
    #dictDoc.write(line[0])
    #dictDoc.write(line[1])
    #dictDoc.write('\n')
    dictDoc.close()
    
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