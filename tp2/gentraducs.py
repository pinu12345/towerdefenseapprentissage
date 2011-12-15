# -*- coding: utf-8 -*-
from editDistance import *
from evalDistance import *
import string, types, numpy, sys, getopt

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

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error.msg:
        print args[0]
        print msg
        sys.exit(2)
    #print args[0]
    txList = []
    txList.append(args[0])
    dict = open('lex.2.tx2fr').readlines()
    output = open('translations.txt', 'w')
    outputprob = open('probabilites.txt', 'w')
    texto = open('originaltexto.txt', 'w')
    texto.write(args[0])
    texto.close()
    txCopy = txList[:]

    seuilAcceptabilite = 0.75
    num_tx = 1

    for i in range(num_tx):
        txCopy[i] = wordSplit(txCopy[i].lower())
        #print txCopy[i]

    for s in range(num_tx):
        # inserer une liste de candidats vide
        candidats = []
        for w in range(len(txCopy[s])):
            word = txCopy[s][w]
            a = 0
            b = len(dict)
            word_found = 0
            while a != b:
                i = (a+b)/2
                ##Split la ligne pour obtenir w1
                dictSplit = dict[i].split(' ')
                w1 = dictSplit[0]
                w2 = dictSplit[1]
                prob = dictSplit[2]
                if w1 == word:
                    a = b
                    word_found = 1
                elif w1 < word:
                    a = i+1
                else:
                    b = i
            if word_found:
                #print 'Word Found :', word
                while 1:
                    if dict[i-1].split(' ')[0] == w1:
                        i -= 1
                    else:
                        break
                trads = dict[i][1]
                taux = 0.0
                while dict[i].split(' ')[0] == w1:
                    trad = dict[i].split(' ')
                    if taux <= seuilAcceptabilite:
                        taux += float(trad[2])
                        #print 'New candidat : ', trad[1], trad[2],
                        candidats = addAll(candidats, trad[1], 2*w)
                    i += 1
                txCopy[s][w] = trad[0]
                #print
            else:
                #print 'Word Not Found :', word
                candidats = addAll(candidats, word, 2*w)

        results = toList(candidats)
        write = ''
        for phrase in results:
            for word in phrase:
                if word == phrase[-1]:
                    write += word + '\n'
                else:
                    write += word + ' '
            output.write(write)
            write = ''

if __name__ == "__main__":
    main()
    
    