import fileinput

def sort_file():
    dict = open('lex.1.f2e').readlines()
    sorted = open('lex.2.tx2fr', 'w')
    lines=[] # give lines variable a type of list
    for line in dict:
        array = line.split(' ')
        lines.append(array[1] + ' ' + str(1 - float(array[2])) + ' ' + array[0])
    lines.sort()
    for line in lines:
        array = line.split(' ')
        sorted.write(array[0] + ' ' + array[2] + ' ' + str(1 - float(array[1])) + '\n')
sort_file()