from params import *
from errors import *

lineCount = 0  # Counting number of lines entered till now
lines = [] #List where commads readd from file are stored
variables = []
commands = []
labels = {}
instrn_count = 0

def splitter():
    f=open("input_file.txt")
    cmd_list=f.readlines()
    cmd_list = [line.strip() for line in cmd_list]
    if len(cmd_list) > 256: #128 given hai
       print("Lines exceed 256")
       exit()
    #print(cmd_list)  

    for i in range(0,len(cmd_list)):
        line=cmd_list[i].split()
        #checking for variable validity
        if line[0] == "var":
            if len(line) == 2:
                if flagVarOver: #flagVarOver define nahi kara, = 0 se initialize kardo
                    print(f"Error: Variables found after the beginning")
                    exit()
                else:
                    var = line[1]
                    if duplicateVar(var):
                        print(f"Error: Duplicate variable name: {var}")
                        exit()
                    else:
                        if varNameValidity(var):
                            variables.append(var)
                            continue
                        else:
                            exit()
            else:
                print(f"General Syntax Error in line {i+1}: ")
                exit()
        else:
            flagVarOver = 1 #1 = True
            
        #checking for label validity        
        if line[0][-1] == ":":
            if not labelValidity(line[0][:-1]):
                exit()
            else:
                labels[line[0][:-1]] = i - len(variables) #Yeh kya hai? #Labels kya hai?
                continue
            
    #checking for validity of other commands
    for cmd in lines[len(variables) :]:
        if ":" in cmd: #cmd me colon kyu hai?
            cmd1 = cmd.split(":")[1].strip()
            if isValidCmd(cmd1):
                if isLineValid(cmd1): #IMP, check this functions in errors.py
                    commands.append(cmd1)
                else:
                    print(f"General Syntax Error on line {lineCount+1}: {cmd}")
                    exit()
            else:
                print(f"General Syntax Error on line {lineCount+1}: {cmd}")
                exit()
        elif isValidCmd(cmd):
            if isLineValid(cmd):
                commands.append(cmd)
            else:
                print(f"General Syntax Error on line {lineCount+1}: {cmd}")
                exit()
        else:
            print("Error: Invalid Command on line " + str(lineCount + 1) + ": " + cmd)
            exit()

    hltCount = 0
    #checking for halt commands
    for c in commands:
        if c == "hlt":
            hltCount += 1

    if hltCount > 1:
        print("Error: More than one hlt instruction found")
        exit()
    elif hltCount == 0:
        print("Error: No hlt instruction found")
        exit()
    elif commands[-1]!="hlt":
        print("Error: hlt should be the last command")
    else:
        for key in labels.keys(): #yeh kya kara??
            labels[key] = make_7bit_binary(labels[key])
    assembleOut(line)

        # for cc in commands:
        #     printbin(cc.split())
        # exit()

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

def typeA(cmd): #the same list given to "assembleOut" is given here
    strout = ""
    strout += opcode[cmd[0]][0]
    strout += "00"
    r1 = registersF[cmd[1]]
    r2 = registersF[cmd[2]]
    r3 = registersF[cmd[3]]
    strout += r1 + r2 + r3
    return strout

#IMP - Move wala case alag se deal in B & C

def typeB(cmd): #the same list given to "assembleOut" is given here
    strout = ""
    strout += opcode[cmd[0]][0]
    strout += "0"
    r1 = registersF[cmd[1]]
    strout += r1
    imm = cmd[2][1:]#as 0 is $
    immbin = make_7bit_binary(int(imm))
    strout += immbin
    return strout

def typeC(cmd): #the same list given to "assembleOut" is given here
    strout = ""
    strout += opcode[cmd[0]][0]
    strout += "00000"
    r1 = registersF[cmd[1]]
    strout += r1
    r2 = registersF[cmd[2]]
    strout += r2
    return strout

def typeD(cmd): #the same list given to "assembleOut" is given here
    strout = ""
    if cmd[-1] in variables:
            for i in range(len(variables)):
                if variables[i] == cmd[-1]:
                    ind = i + len(commands) - 1 #yeh smajh aaya kisi ko?
                    break
            mem_addr = instrn_count + (ind + 1)
            bin_mem_addr = make_7bit_binary(mem_addr)
            strout = opcode[cmd[0]][0] + "0" + registersF[cmd[1]] + bin_mem_addr
    else:
        pass  # handle no variable declared error here?
    return strout

def typeE(cmd): #the same list given to "assembleOut" is given here
    bin_mem_addr = labels[cmd[1]]
    strout = ""
    strout += opcode[cmd[0]][0]
    strout += "0000"
    strout += bin_mem_addr
    return strout

def typeF(cmd): #the same list given to "assembleOut" is given here
    strout = ""
    strout = opcode[cmd[0]][0] + "00000000000"
    return strout

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
    typeF_ins = ["hlt"]
    if (cmd[0] in typeF_ins): return typeF(cmd)
