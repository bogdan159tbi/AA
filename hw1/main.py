# Turing machine accepter
import sys
#func to read tapes from file
#list of dictionaries

def readTapes(f):
    str = f.readline()
    listDex = []
    for x in str.split(" "):
        tape = dict()
        whichPart = 0 #to check if i get the leftword/symbol/rightword
        for word in x.split(","):
            if(whichPart == 0):
                tape["leftW"] = word[1:len(word)]
                whichPart += 1
            elif(whichPart == 1):
                tape["state"] = word
                whichPart += 1
            elif(whichPart == 2):
                tape["rightW"] = word[0:len(word)-1]
                whichPart += 1
        listDex.append(tape)
    return listDex
#done with reading tapes for each exec

#func to read transition
def readTM(f):
    nrStates = f.readline()
    line = f.readline()
    finalStates = []
    for state in line.split(" "):
        if(state != '-'):#daca exista vreo stare finala
            finalStates.append(state)
    Lines = f.readlines()
    listTrans = []
    for line in Lines:
        state = 0
        tape = dict()
        for sign in line.split(" "):
            if( state == 0):
                tape["cState"] = sign
                state += 1
            elif(state == 1):
                tape["cSimb"] = sign
                state += 1
            elif(state == 2):
                state += 1
                tape["nState"] = sign
            elif(state == 3):
                state += 1
                tape["nSimb"] = sign
            elif(state == 4):
                state += 1
                tape["pos"] = sign[0]
        listTrans.append(tape)
    return(nrStates,finalStates,listTrans)

#func to return index from list of dex
def searchDex(list,state,simb):
    index = 0
    #print(state,simb)
    for trans in list:
        if(trans["cSimb"] == simb):
            if(trans["cState"] == state):
                #print("verific: ",trans["cState"],state)
                return index
        index += 1
    print("False",end = " ")
    return -1
#step function
#@tape represents word  to be simulated on
#transitions repr matrix of tm
def step(tape,transitions):
    index = searchDex(transitions,tape["state"],tape["rightW"][0]) #found which transition to make
    if(index == -1):
        return False
    elif(transitions[index]["pos"] == 'R'):
        nextSimb = transitions[index]["nSimb"]
        tape["leftW"] = tape["leftW"] + nextSimb
        tape["rightW"] = tape["rightW"][1:len(tape["rightW"])]
        if(tape["rightW"][0:1] == ''):#daca am depasit toate simbolurile din dreapta
            tape["rightW"] = '#'
        tape["state"] = transitions[index]["nState"]
    elif(transitions[index]["pos"] == 'L'):
        tape["rightW"] = transitions[index]["nSimb"] + tape["rightW"][1:len(tape["rightW"])] #scap de prima litera de la rightw si o inlocuiesc cu urmatorul simbol care trebuie sa suprascrie prima litera de la rightw
        simb = tape["leftW"][len(tape["leftW"])-1]
        #if(tape["leftW"][len(tape["leftW"])-1] == '#'):#trece la simbol # fiind ultimul din stanga
         #tape["leftW"] = '#'#in stanga primului # e tot #
        #else:
            #tape["leftW"] = tape["leftW"][len(tape["leftW"]) - 2 ] # nu stiu sigur daca -2/-1 ca sa scap de ultimul carac de la capatul lui leftW
        tape["leftW"] = tape["leftW"][0:len(tape["leftW"])-1]
        tape["rightW"] = simb + tape["rightW"]
        tape["state"] = transitions[index]["nState"]
    elif(transitions[index]["pos"] == 'H'):
        tape["leftW"] = tape["leftW"]
        tape["rightW"] = transitions[index]["nSimb"] + tape["rightW"][1:len(tape["rightW"])]
        tape["state"] = transitions[index]["nState"]
    if(len(tape["leftW"]) == 0 ):
        tape["leftW"] = "#"
    if(len(tape["rightW"]) == 0 ):
        tape["rightW"] = "#"
    output = '(' + tape["leftW"] + "," + tape["state"] + ',' + tape["rightW"] + ')'
    print(output,end = " ")

#func that checks if tm accepts given word
def accept(word,transitions,finalStates):
    pos = 0
    #pentru ultimul cuvant din list de words care ia si enter
    if(word[len(word)-1] == '\n'):
        word = word[0:len(word)-1]
    state = '0'
    accepts = 0
    while(1):
        found = 0
        for i in finalStates:
            if(i[len(i)-1] == '\n'):
                i = i[0:len(i)-1]
            if(i == state):
                accepts = 1
                break
            else:
                #print("caut",state,word[pos])
                for tran in transitions:
                    cst = tran["cState"]
                    csimb = tran["cSimb"]
                    #print("caut",state,word[pos],cst,csimb)
                    if(cst == state):
                        if(pos >= 0): # index out of range pt urm if la word[pos]
                            if(pos >= len(word)):
                                if(csimb == '#'):
                                    found = 1
                                    word2 = word[0:len(word)] + tran["nSimb"]
                                    word = word2
                                    state = tran["nState"]
                                    if(tran["pos"] == 'R'):
                                        pos += 1
                                    elif(tran["pos"] == 'L'):
                                        pos = pos - 1
                                    break
                            elif(csimb == word[pos]):
                                found = 1
                                if(pos == 0):
                                    word2 =  tran["nSimb"] + word[pos + 1: len(word)]
                                elif(pos == 1):
                                    word2 = word[0] + tran["nSimb"] + word[pos + 1 : len(word)]
                                else:
                                    word2 = word[0:pos-1] + tran["nSimb"] + word[pos + 1 : len(word)]
                                word = word2
                                state = tran["nState"]
                                if(tran["pos"] == 'R'):
                                    pos += 1
                                elif(tran["pos"] == 'L'):
                                    pos = pos - 1
                                #print(state,word[pos])
                                break
                        elif(pos < 0):
                            if(csimb == "#"):
                                    found = 1
                                    word2 = word[0:len(word)] + tran["nSimb"]
                                    word = word2
                                    state = tran["nState"]
                                    if(tran["pos"] == 'R'):
                                        pos += 1
                                    elif(tran["pos"] == 'L'):
                                        pos = pos - 1
                                    break

        if(found == 0):
            break
    #print("am aj la ",word,state,word[pos],pos)

    print(accepts == 1,end = " ")

def k_accept(word,transitions,finalStates,steps):
    pos = 0
    #pentru ultimul cuvant din list de words care ia si enter
    if(word[len(word)-1] == '\n'):
        word = word[0:len(word)-1]
    state = '0'
    accepts = 0
    execSteps = 0
    while(1):
        found = 0
        if(execSteps > int(steps)):
            break
        for i in finalStates:
            if(i[len(i)-1] == '\n'):
                i = i[0:len(i)-1]
            if(i == state):
                accepts = 1
                break
            else:
                #print("caut",state,word[pos])
                if(execSteps > steps):
                    break
                else:
                    for tran in transitions:
                        cst = tran["cState"]
                        csimb = tran["cSimb"]
                        #print("caut",state,word[pos],cst,csimb)
                        if(cst == state):
                            if(pos >= 0):
                                if(pos < len(word)):
                                    if(csimb == word[pos]):
                                        execSteps = execSteps + 1
                                        found = 1
                                        if(pos == 0):
                                            word2 =  tran["nSimb"] + word[1: len(word)]
                                        elif(pos == 1):
                                            word2 = word[0:1] + tran["nSimb"] + word[2:len(word)]
                                        else:
                                            word2 = word[0:pos-1] + tran["nSimb"] + word[pos+1:len(word)]
                                        word = word2
                                        state = tran["nState"]
                                        if(tran["pos"] == 'R'):
                                            pos += 1
                                        elif(tran["pos"] == 'L'):
                                            pos = pos - 1
                                        #print(state,word[pos])
                                        break
                                else:
                                    if(csimb == "#"):
                                        execSteps = execSteps + 1
                                        found = 1
                                        word2 = word[0:len(word)] + tran["nSimb"]
                                        word = word2
                                        state = tran["nState"]
                                        if(tran["pos"] == 'R'):
                                            pos += 1
                                        elif(tran["pos"] == 'L'):
                                            pos = pos - 1
                                        break
                            elif(pos < 0):
                                if(csimb == "#"):
                                    execSteps = execSteps + 1
                                    found = 1
                                    word2 = word[0:len(word)] + tran["nSimb"]
                                    word = word2
                                    state = tran["nState"]
                                    if(tran["pos"] == 'R'):
                                        pos += 1
                                    elif(tran["pos"] == 'L'):
                                        pos = pos - 1
                                    break

        if(found == 0):
            break
    if(execSteps > steps ):
        print("False")
    else:
        print(accepts == 1,word)
def k_accept2(word,transitions,finalStates,steps):
    tape = dict()
    tape["state"] = "0"
    tape["leftW"] = '#'
    tape["rightW"] = word
    for i in range(0,steps):
        step(tape,transitions)


#main
f = open("./tema1_in/k_accept/input/k_accept2.in", "r")
task = f.readline()
task = task[0:len(task)-1]
if(task == "step"):
    listTapes = readTapes(f)
    nrStates, finalStates , listTrans = readTM(f)
    for i in range(0,len(listTapes)):
        step(listTapes[i],listTrans)
elif(task == "accept"):
    words = f.readline()
    nrStates, finalStates , listTrans = readTM(f)
    for word in words.split(' '):
        accept(word,listTrans,finalStates)
elif(task == "k_accept"):
    words = []
    count = [0] * 1000000 #cate cuvinte avem de interpretat pe TM
    elem = 0
    cuvk = f.readline()
    for i in cuvk.split(" "):
        first = 1
        for j in i.split(","):
            if(first == 1):
                words.append(j)
                first = 0
            else:
                if(j[len(j)-1] == '\n'):
                    j = j[0:len(j)-1]
                count[elem] = int(j)
                elem += 1
    nrStates, finalStates , listTrans = readTM(f)
    whichW = 0
    for word in words:
        #print(word,end = " = ")
        k_accept2(word,listTrans,finalStates,count[whichW])
        break
        #print()
        whichW += 1
    #words lista cuvinte si count nr de pasi pt fiecare cuvant corespunzator

f.close()#done reading TM

#while True:
    #data = sys.stdin.read()
    #if not len(data):
    #    break
    #sys.stdout.write(data)

#for line in sys.stdin:
#   if 'q' == line.rstrip():
#       break
 #   print(f'Input : {line[0:len(line)-1]}')

#print("Exit")

#step(listTapes[0],listTrans)
