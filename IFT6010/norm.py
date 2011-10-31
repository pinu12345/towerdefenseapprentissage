# -*- coding: utf-8 -*-
import re
import operator
from editDistance import *

texto = open('train.texto')
norm = open('train.norm','w')
dictionary = {}

#load the normalisations
#for line in open('normalisations.txt'):
    #txt, trans = line.split()
    #dictionary[txt] = trans

#apply them to texto
for line in texto:
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