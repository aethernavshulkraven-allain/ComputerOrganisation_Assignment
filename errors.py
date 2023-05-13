from params import *
from SimpleAssembler import variables, labels


def isValidCmd(line: str):
    cmd = line.split()[0]
    if cmd in opcode.keys():
        return True
    if cmd == "var":
        return True
    return False


def duplicateVar(varName: str, variables: list):
    if varName in variables:
        return True
    else:
        return False


def duplicateLabel(labelName: str):
    pass


def labelValidity(labelName: str):
    if duplicateLabel(labelName):
        return False
    # add other conditions here


def varNameValidity(varName: str):
    if duplicateVar(varName):
        return False
    if varName.isdigit():
        return False
    return True


def regValidity(reg: str):
    if reg in registers.keys():
        return True
    return False


def immediateValidity(imm: str):
    imm = list(imm)
    if imm[0] == "$":
        imm = "".join(imm[1:])
        if imm.isdigit() and (int(imm) in range(0, 256)):
            return True
        else:
            print("Imm more than 8 bits: " + imm)
            return False
    return False


def lenChecker(line: str):
    if isValidCmd(line):
        line = line.split()
        cmd = line[0]
        if cmd == "mov" and immediateValidity(line[2]):
            return True
        elif cmd == "mov" and regValidity(line[2]):
            return True
        elif opcode[cmd][1] == "A" and len(line) == 4:
            return True
        elif opcode[cmd][1] == "B" and len(line) == 3:
            return True
        elif opcode[cmd][1] == "C" and len(line) == 3:
            return True
        elif opcode[cmd][1] == "D" and len(line) == 3:
            return True
        elif opcode[cmd][1] == "E" and len(line) == 2:
            return True
        elif opcode[cmd][1] == "F" and len(line) == 1:
            return True
    return False


def isValidMemAddr(line: str):
    cmd = line.split()[0]
    jumpCommands = ["jmp", "jlt", "jgt", "je"]
    loadStore = ["ld", "st"]
    if cmd in jumpCommands:
        if labelValidity(line[2]):
            return True
    if cmd in loadStore:
        if line[2] in variables:
            return True
    return False


def isLineValid(line: str):
    if lenChecker(line):
        line = line.split()
        cmd = line[0]
        if cmd == "mov":
            if regValidity(line[1]):
                if immediateValidity(line[2]):
                    return True
                elif regValidity(line[2]):
                    return True
                elif line[2] == "FLAGS":
                    return True
                else:
                    return False
            else:
                return False
        if "FLAGS" in line:
            print("Illegal use of FLAGS register. Command: " + line.join())
            return False
        if opcode[cmd][1] == "A":
            if regValidity(line[1]) and regValidity(line[2]) and regValidity(line[3]):
                return True
        elif opcode[cmd][1] == "B":
            if regValidity(line[1]) and immediateValidity(line[2]):
                return True
        elif opcode[cmd][1] == "C":
            if regValidity(line[1]) and regValidity(line[2]):
                return True
        elif opcode[cmd][1] == "D" or opcode[cmd][1] == "E":
            if regValidity(line[1]) and isValidMemAddr(line[2]):
                return True
        elif opcode[cmd][1] == "F":
            if len(line) == 1:
                return True
        else:
            return False


# sample input to test the above functions

# line = "mov R0 R2"
# imm = '$32'
# reg = 'R9'
# reg1 = 'R4'
# varName = 'valala'
# varName2 = '1232'

# print(isValidCmd(line))
# print(isLineValid(line))
# print(isValidMemAddr(line))
# print(lenChecker(line))
# print(immediateValidity(imm))
# print(regValidity(reg))
# print(regValidity(reg1))
# print(varNameValidity(varName))
# print(varNameValidity(varName2))