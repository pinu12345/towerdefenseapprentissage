import re

texto = open('dev.texto')
normin = open('norm.norm')
normout = open('dev.norm','w')
dictionary = {}

#load the normalisations
for line in normin:
    txt, trans = line.split()
    dictionary[txt] = trans


for line in texto:
    words =  re.findall(r"[^\s.,!?;]+|[.,!?;]", line)
    for word in words:
        if word in dictionary:
            normout.write(dictionary[word] + ' ')
        else:
            normout.write(str(word) + ' ')
    normout.write('\n')