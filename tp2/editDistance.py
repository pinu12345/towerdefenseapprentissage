# -*- coding: utf-8 -*-
from numpy import *
import re

def affiche_normList(normList):
    print
    lenMax = 0
    for i in range(len(normList)):
        if len(normList[i][0]) > lenMax:
            lenMax = len(normList[i][0])
    for i in range(len(normList)):
        print "", normList[i][0] + ' '*(lenMax-len(normList[i][0])), \
            "-->", normList[i][1]
    print


def addNorms(txSentence, frSentence):
    ### prend un texto et sa traduction manuelle
    ### renvoie une liste des mots et de leur traduction
    
    tx, fr = 0, 1
    
    sentence = [None]*2
    sentence[tx] = txSentence.lower()
    sentence[fr] = frSentence.lower()
    
    words = [None]*2
    words[tx] = wordSplit(sentence[tx])
    words[fr] = wordSplit(sentence[fr])
    
    align = alignPairs(sentence[tx], sentence[fr])
    wordPairs = []
    if align == 0:
        for i in range(len(words[tx])):
            wordPairs.append([words[tx][i], words[fr][i]])
        return wordPairs
    
    ## Pour chaque numero d'alignement
    ##   On verifie a quels mots il correspond
    ##   S'il correspond a un mot tx
    ##     S'il correspond a un nouveau mot fr
    ##       Alors on l'ajoute le mot fr a la traduction du mot tx
    
    lastWordNum = [None]*2
    wordNum = [None]*2
    word = [None]*2
    charNum = [None]*2
    char = [None]*2
    match = [None]*2
    matches = [None]*2
    
    for s in [tx, fr]:
        wordNum[s] = 0
        lastWordNum[s] = -1
        word[s] = words[s][wordNum[s]]
        charNum[s] = 0
        char[s] = word[s][charNum[s]]
        match[s] = None
        matches[s] = []
    
    wordPairsNum = []
    for i in range(len(words[tx])):
        wordPairsNum.append([])
    
    for n in range(len(align[tx])):
        ## Cet alignement correspond-il a des mots?
        for s in [tx, fr]:
            if charNum[s] == len(word[s]):
                wordNum[s] += 1
                if wordNum[s] < len(words[s]):
                    word[s] = words[s][wordNum[s]]
                charNum[s] = 0
            char[s] = word[s][charNum[s]]
            if align[s][n] == char[s]:
                match[s] = 1
                charNum[s] += 1
            else:
                match[s] = 0
            matches[s].append(match[s])
        ## Si l'alignement coorespond a un mot de tx
        if match[tx]:
            ## Si l'alignement correspond a un nouveau mot fr
            if match[fr] and wordNum[fr] not in wordPairsNum[wordNum[tx]]:
                ## Alors on l'ajoute le mot fr a la traduction du mot tx
                wordPairsNum[wordNum[tx]].append(wordNum[fr])
    
    for i in range(len(words[tx])):
        wordList = []
        for wordNumTemp in wordPairsNum[i]:
            wordList.append(words[fr][wordNumTemp])
        wordPairs.append([words[tx][i], wordList])
    
    for pair in wordPairs:
        if len(pair[fr]) >= 1:
            combinedWords = ''
            for word in pair[fr]:
                combinedWords += word + ' '
            pair[fr] = combinedWords.rstrip()
        else:
            pair[fr] = ""
    
    for i in range(len(wordPairs)-2, -1, -1):
        if wordPairs[i][fr] == wordPairs[i+1][fr]:
            wordPairs[i][tx] += ' ' + wordPairs[i+1][tx]
            wordPairs[i+1:i+2] = []
    
    return wordPairs


def addDictionaryWordsFromSentencePair(tx, fr):
    ### prend un texto et sa traduction manuelle
    ### renvoie une liste des mots et de leur traduction
    
    tx = tx.lower()
    fr = fr.lower()
    
    txWords = wordSplit(tx)
    frWords = wordSplit(fr)
    
    nums = alignNumber(tx, fr)
    if nums == 0:
        normList = []
        for i in range(len(txWords)):
            normList.append([txWords[i], frWords[i]])
        return normList
    numx = nums[0]
    numy = nums[1]
    
    
    # 1
    # associe chaque mot de texto a ses alignements
    tx_to_align = []
    startChar = 0
    for word in txWords:
        curChar = tx.find(word, startChar)
        alignNums = []
        for i in range(curChar, curChar+len(word)):
            alignNums.append(numx[i][1])
        tx_to_align.append([word, alignNums])
        startChar += len(word)
    
    # 2
    # associe chaque alignement a un mot francais
    align_to_fr = []
    curWord = 0
    curChar = 0
    for n in range(len(numy)):
        curWordMod = 0
        if curChar > len(frWords[curWord])-1:
            curChar = 0
            curWord += 1
            if numy[n][1] == ' ':
                curWordMod = 1
        align_to_fr.append([numy[n][0], curWord - curWordMod])
        if numy[n][1] == frWords[curWord][curChar]:
            curChar += 1
    
    # 3
    # associe chaque mot de texto a un mot francais
    alignList = []
    for elem in tx_to_align:
        align_match = -1
        for num in elem[1]:
            i = 0
            while align_match == -1 and i < len(align_to_fr):
                if align_to_fr[i][0] == num:
                    align_match = i
                i += 1
        if align_match >= 0:
            alignList.append(align_to_fr[align_match][0])
        else:
            alignList.append(-1)
    
    for i in range(len(txWords)):
        print "", txWords[i], alignList[i]
    
    if 0:
        #for n in [0, -1]:
        #    num = elem[1][n]
        #    align_match = -1
        #    for i in range(len(align_to_fr)):
        #        if align_to_fr[i][0] == num:
        #            align_match = i
        #            break
        #    if align_match >= 0:
        #        frNumList.append(align_to_fr[align_match][1])
            
        #for num in elem[1]:
        #    align_match = -1
        #    for i in range(len(align_to_fr)):
        #        if align_to_fr[i][0] == num:
        #            align_match = i
        #            break
        #    if align_match >= 0:
        #        frWord_num = align_to_fr[align_match][1]
        #        if frWord_num not in frNumList:
        #            frNumList.append(frWord_num)
        pass
    
    normList = []
    norm = ""
    if len(alignList) > 0:
        for i in range(len(alignList)):
            align_match = -1
            wordNumList = []
            norm = ""
            if alignList[i] != -1:
                for j in range(len(align_to_fr)):
                    if align_to_fr[j][0] == alignList[i]:
                        align_match = j
                        break
            if align_match >= 0:
                if i < len(alignList) - 1:
                    imod = i+1
                    while imod < len(alignList):
                        if alignList[imod] == -1:
                            imod += 1
                        else:
                            break
                    while align_to_fr[align_match][0] < alignList[imod]-1:
                        wordNum = align_to_fr[align_match][1]
                        if wordNum not in wordNumList:
                            wordNumList.append(wordNum)
                        if align_match < len(align_to_fr) -1:
                            align_match += 1
                        else:
                            break
                else:
                    while align_match < len(align_to_fr):
                        wordNum = align_to_fr[align_match][1]
                        if wordNum not in wordNumList:
                            wordNumList.append(wordNum)
                        align_match += 1
                for wordNum in wordNumList:
                    norm = norm + frWords[wordNum] + " "
            normList.append(norm.rsplit())
    
    for i in range(len(txWords)):
        elem = normList[i]
        if len(elem) > 1:
            combinedWords = ""
            for word in elem:
                combinedWords += word + " "
            normList[i] = [txWords[i], combinedWords]
        elif len(elem) == 1:
            normList[i] = [txWords[i], elem[0]]
        else:
            normList[i] = [txWords[i], '']
    
    affichage = 0
    if affichage:
    
        #print
        #for elem in align_to_fr:
        #    print elem[0], elem[1]
        #print
        
        for n in range(2):
            for i in range(len(align_to_fr)):
                print align_to_fr[i][n] %10,
            print
        
        print
        for i in range(len(numx)):
            print numx[i][0],
        print
        for i in range(len(numx)):
            print numx[i][1] % 10,
        print
        
        print
        for j in range(len(numy)):
            print numy[j][0] % 10,
        print
        for j in range(len(numy)):
            print numy[j][1],
        print
        
        # 1: tx_to_align
        print
        for elem in tx_to_align:
            print elem[0], elem[1]
        
        # 2
        print
        lenMax = 0
        for i in range(len(txWords)):
            if len(txWords[i]) > lenMax:
                lenMax = len(txWords[i])
        for i in range(len(txWords)):
            print normList[i][0] + ' '*(lenMax-len(normList[i][0])), \
                "-->", normList[i][1]
    
    # output: la traduction de chaque mot de la 1re liste
    return normList

def wordSplit(sentence):
    ### prend une phrase et retourne une liste de ses mots
    return re.findall(r"[a-zA-Z0-9àâæçéèêëîïôœùûüÿÀÂÆÇÉÈÊËÎÏÔŒÙÜŸ\'\-]+|[^\sa-zA-Z0-9àâæçéèêëîïôœùûüÿÀÂÆÇÉÈÊËÎÏÔŒÙÜŸ\-\']+", sentence)

def alignPairs(x, y):
    ### prend un texto et sa traduction
    ### retourne les numeros d'alignement de chacun
    i, j = len(x), len(y)
    T = editDistance(x, y, table=1)
    
    if T == 0:
        return 0
    
    stepList = editSteps(x, y, T)
    
    #for step in stepList:
    #    print step
    
    numx, numy = [], []
    i, j = 0, 0
    for n in range(len(stepList)):
        if stepList[n][0] != 'I':
            numx.append([x[i], n])
            i += 1
        if stepList[n][0] != 'D':
            numy.append([n, y[j]])
            j += 1
    
    xlist = []
    ylist = []
    i, j = 0, 0
    for step in stepList:
        if step[0] != 'I':
            if i < len(x):
                xlist.append(x[i])
                i += 1
        else:
            xlist.append(' ')
        if step[0] != 'D':
            if j < len(y):
                ylist.append(y[j])
                j += 1
        else:
            ylist.append(' ')

    print '', ''.join(xlist)
    print '', ''.join(ylist)
    
    return [xlist, ylist]
    
def alignNumber(x, y):
    ### prend un texto et sa traduction
    ### retourne les numeros d'alignement de chacun
    i, j = len(x), len(y)
    T = editDistance(x, y, table=1)
    
    if T == 0:
        return 0
    
    stepList = editSteps(x, y, T)
    
    #for step in stepList:
    #    print step
    
    numx, numy = [], []
    i, j = 0, 0
    for n in range(len(stepList)):
        if stepList[n][0] != 'I':
            numx.append([x[i], n])
            i += 1
        if stepList[n][0] != 'D':
            numy.append([n, y[j]])
            j += 1
    
    ## affichage
    affichage = 1
    xlist = [' ']
    ylist = [' ']
    if affichage:
        i, j = 0, 0
        for step in stepList:
            if step[0] != 'I':
                if i < len(x):
                    xlist.append(x[i])
                    i += 1
            else:
                xlist.append(' ')
            if step[0] != 'D':
                if j < len(y):
                    ylist.append(y[j])
                    j += 1
            else:
                ylist.append(' ')
        print
    nlist = [' ']
    for n in range(len(stepList)):
        nlist.append(str(n % 10))
    
    print ''.join(xlist)
    print ''.join(nlist)
    print ''.join(ylist)
    
    return [numx, numy]
    
    
def editSteps(x, y, T):
    ### prend un texto et sa traduction
    ### retourne le tableau des etapes d'edition
    i, j = len(x), len(y)
    
    #for i in range(len(T)):
    #    for j in range(len(T[0])):
    #        print T[i][j] % 10,
    #    print
    #print
    
    if T == 0:
        return 0
    
    stepList = []
    while i > 0 or j > 0:
        if T[i][j] == T[i-1][j]+1:
            i -= 1
            stepList.insert(0, ("Delete " + x[i]))
        elif T[i][j] == T[i][j-1]+1:
            j -= 1
            stepList.insert(0, ("Insert " + y[j]))
        else:
            i -= 1
            j -= 1
            if T[i][j] == T[i+1][j+1]:
                stepList.insert(0, ("Keep   " + x[i]))
            else:
                stepList.insert(0, ("Change " + x[i] + " to " + y[j]))
    return stepList
        

def editDistance(x, y, table=0, align=0):

    if x == y:
        return 0
    
    I, J = len(x)+1, len(y)+1
    T = [[None] * J for i in range(I)]
    #A = [[None] * J for i in range(I)]
    
    for i in range(I):
        T[i][0] = i
        #A[i][0] = 'D'
    for j in range(J):
        T[0][j] = j
        #A[0][j] = 'I'
    #A[0][0] = '-'
    for i in range(1, I):
        for j in range(1, J):
            if x[i-1] == y[j-1]:
                T[i][j] = T[i-1][j-1]
                #A[i][j] = '-'
            else:
                if len(x[i-1]) + len(y[j-1]) > 2:
                    delCost = len(x[i-1])
                    insCost = len(y[j-1])
                    subCost = editDistance(x[i-1], y[j-1])
                else:
                    delCost = insCost = subCost = 1
                delete = T[i-1][j] + delCost
                insert = T[i][j-1] + insCost
                substi = T[i-1][j-1] + subCost
                choices = [delete, insert, substi]
                choice = argmin(choices)
                T[i][j] = choices[choice]
                #if choice == 0:
                #    A[i][j] = 'D'
                #elif choice == 1:
                #    A[i][j] = 'I'
                #else:
                #    A[i][j] = 'S'
                if 0:
                    if T[i-1][j-1] <= T[i-1][j] \
                        and T[i-1][j-1] <= T[i][j-1]:
                        if len(x[i-1]) + len(y[j-1]) > 2:
                            subCost = 1.0 * editDistance(x[i-1], y[j-1]) \
                                / max(len(x[i-1]), len(y[i-1]))
                            print
                            print x[i-1], y[j-1], editDistance(x[i-1], y[j-1])
                            print x[i-1], y[j-1], max(len(x[i-1]), len(y[i-1]))
                            print x[i-1], y[j-1], subCost
                            #subCost = 1
                        else:
                            subCost = 1
                        T[i][j] = T[i-1][j-1] + subCost
                    else:
                        T[i][j] = min( \
                            T[i-1][j] +1, \
                            T[i][j-1] +1)
    
    #print
    #for i in range(0, I):
    #    for j in range(0, J):
    #        print T[i][j] % 10,
    #    print
    #print
    
    if table:
        return T
    elif align:
        return A
    else:
        return T[I-1][J-1]