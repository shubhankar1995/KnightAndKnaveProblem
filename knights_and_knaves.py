# EDIT THE FILE WITH YOUR SOLUTION

from collections import defaultdict
from itertools import product
import re

puzzle_file_name = input('Which text file do you want to use for the puzzle? ')
puzzle_data = (open(puzzle_file_name,"r")).read()

def cleanSencence(puzzle_data):
    puzzle_data = puzzle_data.replace('\n',' ')
    puzzle_data = puzzle_data.replace(',"','"')
    puzzle_data = puzzle_data.replace('!"','"!')
    puzzle_data = puzzle_data.replace('."','".')
    puzzle_data = puzzle_data.replace('?"','"?')
    puzzle_data = puzzle_data.replace(', "','" ')
    #puzzle_data = puzzle_data.replace('! "','"! ')
    #puzzle_data = puzzle_data.replace('. "','". ')
    #puzzle_data = puzzle_data.replace('? "','"? ')
    puzzle_data = puzzle_data.replace(':','')
    return puzzle_data

def getSirs(puzzle_data):
    new_puzzle_data = puzzle_data.replace('?','')
    new_puzzle_data = new_puzzle_data.replace('!',' ')
    new_puzzle_data = new_puzzle_data.replace('.',' ')
    new_puzzle_data = new_puzzle_data.replace('"',' ')
    new_puzzle_data = new_puzzle_data.replace(',',' ')
    a = new_puzzle_data.split()
    sir_list=[]
    end_flag = 2
    i = 0
    while(i < len(a)):
        #print(i)
        if a[i] == 'Sir':
            sir_list.append(a[i+1])
            i = i+1
        elif a[i] == 'Sirs':
            end_flag = 2
            while(i < len(a)):
                if a[i+1] != 'and' and a[i+1] != 'or' and a[i+1].istitle() and end_flag:
                    sir_list.append(a[i+1])
                    #print(a[i+1])
                    i = i+1
                    if end_flag == 1:
                        end_flag = 0
                elif a[i + 1] == 'and' or a[i+1] == 'or':
                    i = i+1
                    #print("entered and/or")
                    end_flag = 1
                elif ',' in a[i+1]:
                    i = i+1
                    #print("entered ,")
                else:
                    #print("getting out")
                    break
        else:
            i = i+1
    sir_list = list(dict.fromkeys(sir_list))
    return sir_list

def getSentences(new_data):
    sentence = new_data.replace('.','<eol>')
    sentence = sentence.replace('!','<eol>')
    sentence = sentence.replace('?','<eol>')
    sentenceList = sentence.split('<eol>')
    return sentenceList

new_data = cleanSencence(puzzle_data)
#print(new_data)
sir_list = getSirs(new_data)
sir_list.sort()
print( 'The Sirs are: '+' '.join(f'{name}' for name in sir_list))

sentenceList = getSentences(new_data)

#print(sentenceList)

sirCount = len(sir_list)

optionTup = list(product((0,1), repeat = sirCount))
optionList = []

for tup in optionTup:
    temp = list(tup)
    temp.append(1)
    optionList.append(temp)

for sentence in sentenceList:
    if '"' in sentence:
        #print(sentence)
        #print(optionList)
        clause = re.findall('"([^"]*)"', sentence)[0]
        speaker = getSirs(sentence.replace(clause, ''))[0]
        #print(f'speaker = {speaker} clause = {clause}')
        clause_sirs = getSirs(clause)
        if 'I' in clause.upper() and not 'sir i' in clause.lower():
            #print("rule 1A")
            clause_sirs.append(speaker)
            clause_sirs = list(dict.fromkeys(clause_sirs))
        if ' us ' in clause.lower() and not 'sir us' in clause.lower():
            #print("rule 1B")
            for sir in sir_list:
                if sir not in clause_sirs:
                    clause_sirs.append(sir)
            clause_sirs = list(dict.fromkeys(clause_sirs))
        if 'knave' in clause.lower() and 'and' not in clause.lower() and ' or ' not in clause.lower() and ' us ' not in clause.lower():
            #print("rule 2")
            for option in optionList:
                if option[sir_list.index(speaker)] == 1:
                    if option[sir_list.index(clause_sirs[0])] == 1:
                        optionList[optionList.index(option)][sirCount] = 0
                elif option[sir_list.index(speaker)] == 0:
                    if option[sir_list.index(clause_sirs[0])] == 0:
                        optionList[optionList.index(option)][sirCount] = 0
        if 'knight' in clause.lower() and 'and' not in clause.lower() and ' or ' not in clause.lower() and ' us ' not in clause.lower():
            #print("rule 3")
            for option in optionList:
                if option[sir_list.index(speaker)] == 1:
                    if option[sir_list.index(clause_sirs[0])] == 0:
                        optionList[optionList.index(option)][sirCount] = 0
                elif option[sir_list.index(speaker)] == 0:
                    if option[sir_list.index(clause_sirs[0])] == 1:
                        optionList[optionList.index(option)][sirCount] = 0
        if 'at least' in clause.lower() and 'one' in clause.lower() and 'knave' in clause.lower():
            #print("rule 4")
            for option in optionList:
                if option[sir_list.index(speaker)] == 1:
                    evalCondition = ''
                    for sir in clause_sirs:
                        evalCondition = evalCondition + str(option[sir_list.index(sir)]) + ' == 1 '
                        if sir not in clause_sirs[len(clause_sirs) - 1]:
                            evalCondition = evalCondition + ' and '
                    tempResult = eval(evalCondition)
                    #print(evalCondition)
                    if tempResult:
                        optionList[optionList.index(option)][sirCount] = 0
                elif option[sir_list.index(speaker)] == 0:
                    evalCondition = ''
                    for sir in clause_sirs:
                        evalCondition = evalCondition + str(option[sir_list.index(sir)]) + ' == 1 '
                        if sir not in clause_sirs[len(clause_sirs) - 1]:
                            evalCondition = evalCondition + ' and '
                    tempResult = eval(evalCondition)
                    #print(evalCondition)
                    if not tempResult:
                        optionList[optionList.index(option)][sirCount] = 0

        if 'at least' in clause.lower() and 'one' in clause.lower() and 'knight' in clause.lower():
            #print("rule 5")
            for option in optionList:
                if option[sir_list.index(speaker)] == 1:
                    evalCondition = ''
                    for sir in clause_sirs:
                        evalCondition = evalCondition + str(option[sir_list.index(sir)]) + ' == 0 '
                        if sir not in clause_sirs[len(clause_sirs) - 1]:
                            evalCondition = evalCondition + ' and '
                    tempResult = eval(evalCondition)
                    #print(evalCondition)
                    if tempResult:
                        optionList[optionList.index(option)][sirCount] = 0
                elif option[sir_list.index(speaker)] == 0:
                    evalCondition = ''
                    for sir in clause_sirs:
                        evalCondition = evalCondition + str(option[sir_list.index(sir)]) + ' == 0 '
                        if sir not in clause_sirs[len(clause_sirs) - 1]:
                            evalCondition = evalCondition + ' and '
                    tempResult = eval(evalCondition)
                    #print(evalCondition)
                    if not tempResult:
                        optionList[optionList.index(option)][sirCount] = 0

        if 'at most' in clause.lower() and 'one' in clause.lower() and 'knave' in clause.lower():
            #print("rule 6")
            for option in optionList:
                tempCount = 0
                for sir in clause_sirs:
                    if option[sir_list.index(sir)] == 0:
                        tempCount = tempCount + 1
                if option[sir_list.index(speaker)] == 1:
                    if not (tempCount <= 1):
                        optionList[optionList.index(option)][sirCount] = 0
                elif option[sir_list.index(speaker)] == 0:
                    if not (tempCount >= 2):
                        optionList[optionList.index(option)][sirCount] = 0

        if 'at most' in clause.lower() and 'one' in clause.lower() and 'knight' in clause.lower():
            #print("rule 7")
            for option in optionList:
                tempCount = 0
                for sir in clause_sirs:
                    if option[sir_list.index(sir)] == 1:
                        tempCount = tempCount + 1
                if option[sir_list.index(speaker)] == 1:
                    if not (tempCount <= 1):
                        optionList[optionList.index(option)][sirCount] = 0
                elif option[sir_list.index(speaker)] == 0:
                    if (tempCount <= 1):
                        optionList[optionList.index(option)][sirCount] = 0

        if 'exactly' in clause.lower() and 'one' in clause.lower() and 'knave' in clause.lower():
            #print("rule 8")
            for option in optionList:
                tempCount = 0
                for sir in clause_sirs:
                    if option[sir_list.index(sir)] == 0:
                        tempCount = tempCount + 1
                if option[sir_list.index(speaker)] == 1:
                    if not (tempCount == 1):
                        optionList[optionList.index(option)][sirCount] = 0
                elif option[sir_list.index(speaker)] == 0:
                    if (tempCount == 1):
                        optionList[optionList.index(option)][sirCount] = 0

        if 'exactly' in clause.lower() and 'one' in clause.lower() and 'knight' in clause.lower():
            #print("rule 9")
            for option in optionList:
                tempCount = 0
                for sir in clause_sirs:
                    if option[sir_list.index(sir)] == 1:
                        tempCount = tempCount + 1
                if option[sir_list.index(speaker)] == 1:
                    if not (tempCount == 1):
                        optionList[optionList.index(option)][sirCount] = 0
                elif option[sir_list.index(speaker)] == 0:
                    if (tempCount == 1):
                        optionList[optionList.index(option)][sirCount] = 0

        if 'all' in clause.lower() and 'us' in clause.lower() and 'knave' in clause.lower():
            #print("rule 10")
            for option in optionList:
                if option[sir_list.index(speaker)] == 1:
                    evalCondition = ''
                    for sir in clause_sirs:
                        evalCondition = evalCondition + str(option[sir_list.index(sir)]) + ' == 0 '
                        if sir not in clause_sirs[len(clause_sirs) - 1]:
                            evalCondition = evalCondition + ' and '
                    tempResult = eval(evalCondition)
                    #print(evalCondition)
                    if not tempResult:
                        optionList[optionList.index(option)][sirCount] = 0
                elif option[sir_list.index(speaker)] == 0:
                    evalCondition = ''
                    for sir in clause_sirs:
                        evalCondition = evalCondition + str(option[sir_list.index(sir)]) + ' == 0 '
                        if sir not in clause_sirs[len(clause_sirs) - 1]:
                            evalCondition = evalCondition + ' and '
                    tempResult = eval(evalCondition)
                    #print(evalCondition)
                    if tempResult:
                        optionList[optionList.index(option)][sirCount] = 0

        if 'all' in clause.lower() and 'us' in clause.lower() and 'knight' in clause.lower():
            #print("rule 11")
            for option in optionList:
                if option[sir_list.index(speaker)] == 1:
                    evalCondition = ''
                    for sir in clause_sirs:
                        evalCondition = evalCondition + str(option[sir_list.index(sir)]) + ' == 1 '
                        if sir not in clause_sirs[len(clause_sirs) - 1]:
                            evalCondition = evalCondition + ' and '
                    tempResult = eval(evalCondition)
                    #print(evalCondition)
                    if not tempResult:
                        optionList[optionList.index(option)][sirCount] = 0
                elif option[sir_list.index(speaker)] == 0:
                    evalCondition = ''
                    for sir in clause_sirs:
                        evalCondition = evalCondition + str(option[sir_list.index(sir)]) + ' == 1 '
                        if sir not in clause_sirs[len(clause_sirs) - 1]:
                            evalCondition = evalCondition + ' and '
                    tempResult = eval(evalCondition)
                    #print(evalCondition)
                    if tempResult:
                        optionList[optionList.index(option)][sirCount] = 0

        if 'knave' in clause.lower() and ' or ' in clause.lower() and 'exactly' not in clause.lower() and 'at most' not in clause.lower() and 'at least' not in clause.lower() and 'all' not in clause.lower():
            #print("rule 12")
            for option in optionList:
                if option[sir_list.index(speaker)] == 1:
                    evalCondition = ''
                    for sir in clause_sirs:
                        evalCondition = evalCondition + str(option[sir_list.index(sir)]) + ' == 1 '
                        if sir not in clause_sirs[len(clause_sirs) - 1]:
                            evalCondition = evalCondition + ' and '
                    tempResult = eval(evalCondition)
                    #print(evalCondition)
                    if tempResult:
                        optionList[optionList.index(option)][sirCount] = 0
                elif option[sir_list.index(speaker)] == 0:
                    evalCondition = ''
                    for sir in clause_sirs:
                        evalCondition = evalCondition + str(option[sir_list.index(sir)]) + ' == 1 '
                        if sir not in clause_sirs[len(clause_sirs) - 1]:
                            evalCondition = evalCondition + ' and '
                    tempResult = eval(evalCondition)
                    #print(evalCondition)
                    if not tempResult:
                        optionList[optionList.index(option)][sirCount] = 0

        if 'knight' in clause.lower() and ' or ' in clause.lower() and 'exactly' not in clause.lower() and 'at most' not in clause.lower() and 'at least' not in clause.lower() and 'all' not in clause.lower():
            #print("rule 13")
            for option in optionList:
                if option[sir_list.index(speaker)] == 1:
                    evalCondition = ''
                    for sir in clause_sirs:
                        evalCondition = evalCondition + str(option[sir_list.index(sir)]) + ' == 0 '
                        if sir not in clause_sirs[len(clause_sirs) - 1]:
                            evalCondition = evalCondition + ' and '
                    tempResult = eval(evalCondition)
                    #print(evalCondition)
                    if tempResult:
                        optionList[optionList.index(option)][sirCount] = 0
                elif option[sir_list.index(speaker)] == 0:
                    evalCondition = ''
                    for sir in clause_sirs:
                        evalCondition = evalCondition + str(option[sir_list.index(sir)]) + ' == 0 '
                        if sir not in clause_sirs[len(clause_sirs) - 1]:
                            evalCondition = evalCondition + ' and '
                    tempResult = eval(evalCondition)
                    #print(evalCondition)
                    if not tempResult:
                        optionList[optionList.index(option)][sirCount] = 0
        
        if 'knave' in clause.lower() and 'and' in clause.lower() and 'exactly' not in clause.lower() and 'at most' not in clause.lower() and 'at least' not in clause.lower() and 'all' not in clause.lower():
            #print("rule 14")
            for option in optionList:
                if option[sir_list.index(speaker)] == 1:
                    evalCondition = ''
                    for sir in clause_sirs:
                        evalCondition = evalCondition + str(option[sir_list.index(sir)]) + ' == 0 '
                        if sir not in clause_sirs[len(clause_sirs) - 1]:
                            evalCondition = evalCondition + ' and '
                    tempResult = eval(evalCondition)
                    #print(evalCondition)
                    if not tempResult:
                        optionList[optionList.index(option)][sirCount] = 0
                elif option[sir_list.index(speaker)] == 0:
                    evalCondition = ''
                    for sir in clause_sirs:
                        evalCondition = evalCondition + str(option[sir_list.index(sir)]) + ' == 0 '
                        if sir not in clause_sirs[len(clause_sirs) - 1]:
                            evalCondition = evalCondition + ' and '
                    tempResult = eval(evalCondition)
                    #print(evalCondition)
                    if tempResult:
                        optionList[optionList.index(option)][sirCount] = 0
        if 'knight' in clause.lower() and 'and' in clause.lower() and 'exactly' not in clause.lower() and 'at most' not in clause.lower() and 'at least' not in clause.lower() and 'all' not in clause.lower():
            #print("rule 15")
            for option in optionList:
                if option[sir_list.index(speaker)] == 1:
                    evalCondition = ''
                    for sir in clause_sirs:
                        evalCondition = evalCondition + str(option[sir_list.index(sir)]) + ' == 1 '
                        if sir not in clause_sirs[len(clause_sirs) - 1]:
                            evalCondition = evalCondition + ' and '
                    tempResult = eval(evalCondition)
                    #print(evalCondition)
                    if not tempResult:
                        optionList[optionList.index(option)][sirCount] = 0
                elif option[sir_list.index(speaker)] == 0:
                    evalCondition = ''
                    for sir in clause_sirs:
                        evalCondition = evalCondition + str(option[sir_list.index(sir)]) + ' == 1 '
                        if sir not in clause_sirs[len(clause_sirs) - 1]:
                            evalCondition = evalCondition + ' and '
                    tempResult = eval(evalCondition)
                    #print(evalCondition)
                    if tempResult:
                        optionList[optionList.index(option)][sirCount] = 0


#print(optionList)

optionCount = 0
for option in optionList:
    if option[sirCount] == 1:
        optionCount = optionCount + 1
        #print(option)

if optionCount == 0:
    print('There is no solution.')
elif optionCount == 1:
    print('There is a unique solution:')
    for option in optionList:
        if option[sirCount] == 1:
            legend = ['Knave','Knight']
            for sir in sir_list:
                print(f'Sir {sir} is a {legend[option[sir_list.index(sir)]]}.')
else:
    print(f'There are {optionCount} solutions.')
