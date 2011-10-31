# -*- coding: utf-8 -*-
from editDistance import *
from evalDistance import *

tx = "pcqz jwvaiys X liavnir 2m1"
fr = "Parce que je vais la voir demain."

align(tx, fr)

    
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






    x = "Sa srait cool de srtr"
    y = "Ca serait cool de sortir."

    #x = ["Sa", "srait", "cool", "de", "srtr"]
    #y = ["Ça", "serait", "cool", "de", "sortir", "."]

    x = ["La", "di", "stance", "devrait", "être", "cinq", "."]
    y = ["La", "distance", "devrait", "être", "cinq", "."]

    x = "La di stance devrait être cinq. La di stance devrait être cinq. La di stance devrait être cinq. La di stance devrait être cinq. La di stance devrait être cinq. La di stance devrait être cinq."
    y = "La distance devrait être cinq. La distance devrait être cinq. La distance devrait être cinq. La distance devrait être cinq. La distance devrait être cinq. La distance devrait être cinq."


    print
    print editDistance(x, y)