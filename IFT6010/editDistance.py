# -*- coding: utf-8 -*-
from numpy import *
import re

def align(tx, fr):
    # input: 2 phrases
    
    nums = alignNumber(tx, fr)
    numx = nums[0]
    numy = nums[1]
    
    txWords = wordSplit(tx)
    frWords = wordSplit(fr)
    
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
    
    # associe chaque alignement a un mot francais
    align_to_fr = []
    curWord = 0
    curChar = 0
    for a in range(len(numy)):
        align_to_fr.append([numy[a][0], curWord])
        curChar += 1
        if curChar > len(frWords[curWord]):
            curChar = 0
            curWord += 1
    
    # associe chaque mot de texto a un mot francais
    normList = []
    for elem in tx_to_align:
        frNumList = []
        for num in elem[1]:
            align_match = -1
            for i in range(len(align_to_fr)):
                if align_to_fr[i][0] == num:
                    align_match = i
                    break
            if align_match >= 0:
                frWord_num = align_to_fr[align_match][1]
                if frWord_num not in frNumList:
                    frNumList.append(frWord_num)
            
        norm = ""
        if len(frNumList) > 0:
            for frNum in frNumList:
                norm = norm + frWords[frNum] + " "
        else:
            norm = ""
            
        normList.append(norm.rsplit())
        
    #print
    #for elem in align_to_fr:
    #    print elem[0], elem[1]
    #print
    
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
    
    print
    for elem in tx_to_align:
        print elem[0], elem[1]
    
    print
    for i in range(len(txWords)):
        print txWords[i], normList[i]
    
    
    # output: la traduction de chaque mot de la 1re liste
    ## align

def wordSplit(sentence):
    return re.findall(r"[a-zA-Z0-9àâæçéèêëîïôœùûüÿÀÂÆÇÉÈÊËÎÏÔŒÙÜŸ]+|[^\sa-zA-Z0-9àâæçéèêëîïôœùûüÿÀÂÆÇÉÈÊËÎÏÔŒÙÜŸ]+", sentence)

def alignNumber(x, y):
    i, j = len(x), len(y)
    T = editDistance(x, y, table=1)
    
    stepList = editSteps(x, y)
    
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
    if affichage:
        i = 0
        for step in stepList:
            if step[0] != 'I':
                if i < len(x):
                    print x[i],
                    i += 1
            else:
                print ' ',
        print
        i = 0
        for step in stepList:
            if step[0] != 'D':
                if i < len(y):
                    print y[i],
                    i += 1
            else:
                print ' ',
        print
    
    return [numx, numy]
    
    
def editSteps(x, y):
    i, j = len(x), len(y)
    T = editDistance(x, y, table=1)
    
    #for i in range(len(T)):
    #    for j in range(len(T[0])):
    #        print T[i][j] % 10,
    #    print
    
    stepList = []
    print
    while i > 0 and j > 0:
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