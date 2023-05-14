from params import *
#from errors import *

lineCount = 0  # Counting number of lines entered till now
lines = [] #List where commads readd from file are stored
variables = []
labels = {}
instrn_count = 0

#Things To Be Edited - Modify post this comment for the ones that are done/assigned
#Params - Done by aarya
#typeA, typeB, make_7bit_binary, assembleout functions done by Arnav Shukla

def make_7bit_binary(num):
    con_num = []
    while num >= 1:
        rem = num % 2
        con_num.append(str(int(rem)))
        num = num // 2
    con_num = con_num[::-1]
    bin = "".join(con_num)
    if len(bin) < 7:
        bin = "0" * (7 - len(bin)) + bin
    return bin

def assembleOut(cmd):
    #if encountered type is A
    typeA_ins = ["add", "sub", "mul", "xor", "or", "and"]
    if (cmd[0] in typeA_ins): return typeA(cmd)

    #if encountered type is B
    typeB_ins = ["mov", "rs", "ls"]
    if((cmd[0] in typeB_ins) and ('$' in cmd[2])): return typeB(cmd)

    #if encountered type is C
    typeC_ins = ["mov", "div", "not", "cmp"]
    if (cmd[0] in typeC_ins): return typeC(cmd)

    #if encountered type is D
    typeD_ins = ["ld", "st"]
    if (cmd[0] in typeD_ins): return typeD(cmd)

    #if encountered type is E
    typeE_ins = ["jmp", "jlt", "jgt", "je"]
    if (cmd[0] in typeE_ins): return typeE(cmd)

    #if encountered type is F
    typeF_ins = ["je", "hlt"]
    if (cmd[0] in typeF_ins): return typeF(cmd)

def typeA(cmd):#the same list given to "assembleOut" is given here
    strout = ""
    strout += opcode[cmd[0]][0]
    strout += "00"
    r1 = registersF[cmd[1]]
    r2 = registersF[cmd[2]]
    r3 = registersF[cmd[3]]
    strout += r1 + r2 + r3
    return strout

def typeB(cmd):#the same list given to "assembleOut" is given here
    strout = ""
    strout += opcode[cmd[0]][0]
    strout += "0"
    r1 = registersF[cmd[1]]
    strout += r1
    imm = cmd[2][1:]#as 0 is $
    immbin = make_7bit_binary(int(imm))
    strout += immbin
    return strout