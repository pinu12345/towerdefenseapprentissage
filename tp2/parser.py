# -*- coding: utf-8 -*-
from editDistance import *
import string, types, numpy, sys, getopt, numpy

dictfr2tx = open('lex.2.fr2tx').readlines()
dicttx2fr = open('lex.2.tx2fr').readlines()
ori = open('originaltexto.txt').readline()
addX = 0.0001
lam = 4
phi = 0.0

def main():
    logprobs = open('logprobs.txt').readlines()
    bestprob = -9999999999999
    besttrad = ''
    #print ori
    for i in range(len(logprobs)):
        if i%4 == 0:
            trad = logprobs[i].strip()
        if i%4 == 2:
            logprob = logprobs[i].split('logprob= ')[1].split(' ppl')[0]
            probT = probTrad(trad, ori, dictfr2tx)
            probP = probTrad(ori, trad, dicttx2fr)
            prob = float(logprob) * lam + numpy.log10(probT) + phi * numpy.log10(probP)
            #print trad, prob
            if prob > bestprob:
                bestprob = float(prob)
                besttrad = trad
    print besttrad
    
def probTrad(wfrom, wto, dict):
    #print trad
    wordsfr = wordSplit(wfrom.lower())
    wordstx = wordSplit(wto.lower())

    if len(wordsfr) != len(wordstx):
        return 1.0

    proba = 1.0
    for i in range(len(wordsfr)):
        #print wordsfr[i], wordstx[i]
        wordfr = wordsfr[i]
        wordtx = wordstx[i]
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
            if w1 == wordfr:
                a = b
                word_found = 1
            elif w1 < wordfr:
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
            taux = 0.0
            while dict[i].split(' ')[0] == w1:
                if dict[i].split(' ')[1] == wordtx:
                    #print w1, dict[i].split(' ')[1], dict[i].split(' ')[2]
                    taux = float(dict[i].split(' ')[2])
                i += 1
            taux += addX
            proba *= taux
        else:
            proba *= addX
    #print proba
    return proba
    
if __name__ == "__main__":
    main()