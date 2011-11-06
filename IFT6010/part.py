# -*- coding: utf-8 -*-
from dictMaker import *
from dictTrad import *
from editDistance import *
import string

#str = '"lol'
#print str.replace('"', '\\"')
#print string.replace(str, '"', '\\"')
#print wordSplit('après')

makeDict('train.texto', 'train.fr')
#for line in dict:
#    print '', line[0], '', line[1]