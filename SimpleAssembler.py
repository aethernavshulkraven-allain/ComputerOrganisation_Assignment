from params import *
from errors import *

lineCount = 0  # Counting number of lines entered till now
lines = []
variables = []
labels = {}
instrn_count = 0

#To Be Edited - Modify this comment for the one that are done
#Params - Done

def printbin(lst):
    code = lst[0]
    val = ""
    # A
    if code == "add":
        val = (
            opcode[code][0]
            + "00"
            + registersF[lst[1]]
            + registersF[lst[2]]
            + registersF[lst[3]]
        )

    elif code == "sub":
        val = (
            opcode[code][0]
            + "00"
            + registersF[lst[1]]
            + registersF[lst[2]]
            + registersF[lst[3]]
        )

    elif code == "mul":
        val = (
            opcode[code][0]
            + "00"
            + registersF[lst[1]]
            + registersF[lst[2]]
            + registersF[lst[3]]
        )

    elif code == "xor":
        val = (
            opcode[code][0]
            + "00"
            + registersF[lst[1]]
            + registersF[lst[2]]
            + registersF[lst[3]]
        )

    elif code == "or":
        val = (
            opcode[code][0]
            + "00"
            + registersF[lst[1]]
            + registersF[lst[2]]
            + registersF[lst[3]]
        )

    elif code == "and":
        val = (
            opcode[code][0]
            + "00"
            + registersF[lst[1]]
            + registersF[lst[2]]
            + registersF[lst[3]]
        )

    # B,C

    elif code == "mov":
        if lst[-1][0] == "$":
            needed_num = int(lst[-1][1:])
            final_bin = make_8_bit(needed_num)
            val = opcode[code][0][0] + registersF[lst[1]] + final_bin

        else:
            val = opcode[code][1][0] + "00000" + registersF[lst[1]] + registersF[lst[2]]

    elif code == "div":
        val = opcode[code][0] + "00000" + registersF[lst[1]] + registersF[lst[2]]

    elif code == "not":
        val = opcode[code][0] + "00000" + registersF[lst[1]] + registersF[lst[2]]

    elif code == "cmp":
        val = opcode[code][0] + "00000" + registersF[lst[1]] + registersF[lst[2]]

    elif code == "ls":
        needed_num = int(lst[-1][1:])
        final_bin = make_8_bit(needed_num)
        val = opcode[code][0][0] + registersF[lst[1]] + final_bin

    elif code == "rs":
        needed_num = int(lst[-1][1:])
        final_bin = make_8_bit(needed_num)
        val = opcode[code][0][0] + registersF[lst[1]] + final_bin

    # F
    elif code == "hlt":
        val = opcode[code][0] + "00000000000"

    # D
    elif code == "ld":
        if lst[-1] in variables:
            for i in range(len(variables)):
                if variables[i] == lst[-1]:
                    ind = i + len(commands) - 1
                    break
            mem_addr = instrn_count + (ind + 1)
            bin_mem_addr = make_8_bit(mem_addr)
            val = opcode[code][0] + registersF[lst[1]] + bin_mem_addr
        else:
            pass  # handle no variable declared error here?

    elif code == "st":
        if lst[-1] in variables:
            for i in range(len(variables)):
                if variables[i] == lst[-1]:
                    ind = i + len(commands) - 1
                    break
            mem_addr = instrn_count + (ind + 1)
            bin_mem_addr = make_8_bit(mem_addr)
            val = opcode[code][0] + registersF[lst[1]] + bin_mem_addr
        else:
            pass  # handle no variable declared error here?

    # E
    elif code == "jmp":
        bin_mem_addr = labels[lst[1]]

        val = opcode[code][0] + "000" + bin_mem_addr

    elif code == "jlt":
        bin_mem_addr = labels[lst[1]]

        val = opcode[code][0] + "000" + bin_mem_addr

    elif code == "jgt":
        bin_mem_addr = labels[lst[1]]

        val = opcode[code][0] + "000" + bin_mem_addr

    elif code == "je":
        bin_mem_addr = labels[lst[1]]

        val = opcode[code][0] + "000" + bin_mem_addr

    print(val)