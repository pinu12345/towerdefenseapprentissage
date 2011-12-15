import fileinput

def sort_file():
    dict = open('lex.1.e2f').readlines()
    sorted = open('lex.2.e2f', 'w')
    lines=[] # give lines variable a type of list
    for line in dict: lines.append(line)
    lines.sort()
    for line in lines: sorted.write(line)
sort_file()