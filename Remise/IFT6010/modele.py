# -*- coding: utf-8 -*-
import re, json, operator
from editDistance import *

frList = open('train.fr').readlines()
norm = open('train.norm', 'w')
n = 3
dict = []

for num_tx in [len(frList)]:
#for num_tx in [5]:
    num_tx = min(num_tx, len(frList))
    for i in range(num_tx):
        #print "\n--- Texto", i+1 , "---\n"
        fr = frList[i]
        #print fr
        words =  re.findall(r"[a-zA-Z0-9àâæçéèêëîïôœùûüÿÀÂÆÇÉÈÊËÎÏÔŒÙÜŸ]+|[^\sa-zA-Z0-9àâæçéèêëîïôœùûüÿÀÂÆÇÉÈÊËÎÏÔŒÙÜŸ]+", fr)
        #print len(words)
        for i in range(len(words)):
            ngram = []
            for j in range(n-1,0,-1):
                if i-j < 0:
                    ngram.append('BOS')
                else:
                    ngram.append(words[i-j])
            txWordNotFound = 1
            for line in dict:
                if words[i] == line[0]:
                    txWordNotFound = 0
                    txWordLine = line
                    #print line
                    break
            if txWordNotFound:
                # Ajoute un mot inexistant
                # print([words[i], [ngram]])
                ngram.append(1)
                dict.append([words[i], [ngram]])
                dict.sort()
            else:
                #print('-------------------')
                #print('Already in list : ' + words[i])
                # verifie si ngram existe deja
                ngramNotFound = 1
                #print txWordLine[1]
                #continue
                for frTrad in txWordLine[1]:
                    #print('====')
                    #print frTrad[:-1]
                    #print frTrad[n-1]
                    #print ngram
                    if ngram == frTrad[:-1]:
                        #print('Found')
                        frTrad[n-1] += 1
                        ngramNotFound = 0
                        break
                if ngramNotFound:
                    #print('Not found')
                    ngram.append(1)
                    txWordLine[1].append(ngram)
                    #txWordLine[1].append([ngram])

#json.dump(dict, norm)

if 1 :
    for i in range(len(dict)):
        if i == 0:
            norm.write('[')
        norm.write('["' + dict[i][0].replace('\\','\\\\').replace('"', '\\"') + '", [')
        for j in range(len(dict[i][1])):
            norm.write('["' + dict[i][1][j][0].replace('\\','\\\\').replace('"', '\\"') + '", "' + dict[i][1][j][1].replace('\\','\\\\').replace('"', '\\"') + '", ' + str(dict[i][1][j][2]) + ']')
            if j != len(dict[i][1])-1:
                norm.write(', ')
            else:
                norm.write(']')
        norm.write(']')
        if i != len(dict)-1:
            norm.write(', \n')
        else:
            norm.write(']')
        
if 0:
        for j in range(len(wordPairs)):
            txWord, frWord = wordPairs[j][0], wordPairs[j][1]
            #if txWord != frWord:
            if 1:
                #print(txWord, frWord)
                # cherche txWord dans dict
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






if 0 :
    #apply them to texto
    texto = open('train.texto')
    norm.write(str(n) + '-gram = [\n')
    for line in texto:
        words =  re.findall(r"[a-zA-Z0-9àâæçéèêëîïôœùûüÿÀÂÆÇÉÈÊËÎÏÔŒÙÜŸ]+|[^\sa-zA-Z0-9àâæçéèêëîïôœùûüÿÀÂÆÇÉÈÊËÎÏÔŒÙÜŸ]+", line)
        for i in range(len(words)):
            ngram = []
            if n == 1:
                norm.write(words[i])
            else:
                norm.write(words[i] + ' | ')
            for j in range(n-1,0,-1):
                if i-j < 0:
                    norm.write('BOS ')
                else:
                    norm.write(words[i-j] + ' ')
                #if j == n-1:
                    #norm.write(words[i+j] + ' | ')
                #else:
                    #norm.write(words[i+j] + ' ')
            norm.write('\n')
    norm.write(']\n')