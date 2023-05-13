from params import *
#from errors import *

lineCount = 0  # Counting number of lines entered till now
lines = [] #List where commads readd from file are stored
variables = []
labels = {}
instrn_count = 0

# typeA and typeB function done by Arnav Shukla
def typeA(cmd):#the same list given to "assembleOut" is given here
    strout = ""
    strout += opcode[cmd[0]][0]
    strout += "00"
    r1 = registersF[cmd[1]]
    r2 = registersF[cmd[2]]
    r3 = registersF[cmd[3]]
    strout += r1 + r2 + r3
    return strout

def typeB(cmd)#the same list given to "assembleOut" is given here
    strout = ""
    strout += opcode[cmd[0]][0]
    strout += "0"
    r1 = registersF[cmd[1]]
    strout += r1
    imm = cmd[2][1:]#as 0 is $
    immbin = make_7bit_binary(int(imm))
    strout += immbin
    return strout
#Things To Be Edited - Modify post this comment for the ones that are done/assigned
#Params - Done by aarya
#Type AB - Pending @aarya commit karde 