import re

texto = open('dev.texto')
norm = open('dev.norm','w')
dictionary = {}

#load the normalisations
for line in open('normalisations.txt'):
    txt, trans = line.split()
    dictionary[txt] = trans


for line in texto:
    words =  re.findall(r"[^\s.,!?;]+|[.,!?;]", line)
    for word in words:
        if word in dictionary:
            norm.write(dictionary[word] + ' ')
        else:
            norm.write(str(word) + ' ')
    norm.write('\n')