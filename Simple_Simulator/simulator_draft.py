# *********************** IMPORTS *****************************
import sys

# *********************** REGS *****************************
# Register File (RF): The RF takes in the register name (R0, R1, ... R6 or FLAGS) and
# returns the value stored at that register.
# here R is the RF

R = {
    "000": 0,
    "001": 0,
    "010": 0,
    "011": 0,
    "100": 0,
    "101": 0,
    "110": 0,
    "111": 0,
}


opc = {
    "00000": "A",
    "00001": "A",
    "00010": "B",
    "00011": "C",
    "00100": "D",
    "00101": "D",
    "00110": "A",
    "00111": "C",
    "01000": "B",
    "01001": "B",
    "01010": "A",
    "01011": "A",
    "01100": "A",
    "01101": "C",
    "01110": "C",
    "01111": "E",
    "11100": "E",
    "11101": "E",
    "11111": "E",
    "11010": "F",
}

# *********************** CONVERSIONS *****************************

def binaryToInteger(binStr): #binary to integer
    return int(binStr, 2)

def integerToBinary(intVal, bitSize): #integer to binary
    binStr = bin(intVal)[2:]
    if bitSize > len(binStr):
        binStr = "0" * (bitSize - len(binStr)) + binStr
    else:
        binStr = binStr[(len(binStr) - bitSize) :]
    return binStr

# ************************ BHAI YE CHAHIYE Q2 KE LIYE?, PLS CONFIRM! ***************************

# def floatValidity(imm: str):
#     imm = list(imm)
#     if imm[0] == "$":
#         try:
#             imm = float("".join(imm[1:]))
#             if (
#                 type(imm) == float
#             ):  # ADD and imm in range(), the range of mantissa and exponent
#                 return True
#         except ValueError:
#             print("Invalid immediate.")
#             return False
#     return False

# *************************** MEM *****************************

# Memory (MEM): MEM takes in an 7 bit address and returns a 16 bit value as the data.
# The MEM stores 256 bytes, initialized to 0s.

class memHandler:
    TOT_SIZE = 128
    mem = ["0000000000000000"] * TOT_SIZE

    def load(self, inputFile):
        for index, line in enumerate(inputFile):
            self.mem[index] = line.rstrip("\n")

    def getInst(self, pc): # this provides instruction of the respective PC
        return self.mem[pc]

    def getValueAtAdd(self, memAdd):
        return binaryToInteger(self.mem[binaryToInteger(memAdd)])

    def loadValueAtAdd(self, memAdd, val):
        self.mem[binaryToInteger(memAdd)] = integerToBinary(val, 16)

    def dump(self):
        for Address in self.mem:
            sys.stdout.write(Address + "\n")


PC = 0 #Program Counter (PC): The PC is an 7 bit register which points to the current instruction.
Cycle = 0
Cycle = -1
temp = []

hltFlag = 0

memFile = memHandler()
memFile.load(sys.stdin)

# ******************************** EE *******************************

# Execution Engine (EE): The EE takes the address of the instruction from the PC, uses it
# to get the stored instruction from MEM, and executes the instruction by updating the RF
# and PC.

def floatToDec(binNum: str):
    exp = binNum[:3]
    mantissa = binNum[3:]
    exp = bin(binaryToInteger(exp))[2:]
    mantissa = "1" + "".join(mantissa)
    dec = binaryToInteger(mantissa[: -(len(exp))])
    exp = list(exp)
    exp = [int(i) for i in exp]
    res = 0
    idx = 1
    for i in exp:
        res += (i * 2) ** (-idx)
        idx += 1
    return dec + res


def resetFlag(): # !!!!!!!!!!!!!!! PLS EXPLAIN THE PURPOSE OF THIS !!!!!!!!!!!!!!!!
    R["111"] = 0


def findOpcodeType(op_bin):  # takes the opcode in binary
    return opc[op_bin]


def movImm(reg1, imm):  # assuming immediate is already a decimal here
    R[reg1] = imm
    resetFlag()
    dump()


def movReg(reg1, reg2):
    R[reg2] = R[reg1]
    resetFlag()
    dump()


def add(reg1, reg2, reg3):
    R[reg1] = R[reg2] + R[reg3]
    if R[reg1] > 65535:
        R[reg1] = R[reg1] % 65535  # make all bits 1 in reg1
        R["111"] = 8  # setting overflow flag
        dump()
    else:
        resetFlag()
        dump()


def sub(reg1, reg2, reg3):
    R[reg1] = R[reg2] - R[reg3]
    if R[reg1] < 0:
        R[reg1] = 0  # case of underflow
        R["111"] = 8  # setting overflow flag
        dump()
    else:
        resetFlag()
        dump()


def OR(reg1, reg2, reg3):
    R[reg1] = R[reg2] | R[reg3]
    resetFlag()
    dump()


def mul(r1, r2, r3):
    R[r1] = R[r2] * R[r3]
    if R[r1] > 65535:
        R[r1] = R[r1] % 65535
        R["111"] = 8  # Raise OVERFLOW flag
        dump()
    else:
        resetFlag()
        dump()


def divide(r1, r2):
    R["000"] = int(R[r1] / R[r2])
    R["001"] = int(R[r1] % R[r2])
    if R[r1] < 0:
        R["000"] = 0  # case of underflow
        R["111"] = 8  # Raise OVERFLOW flag
        dump()
    else:
        resetFlag()
        dump()


def rShift(r1, imm):
    R[r1] = R[r1] >> imm
    if R[r1] < 0:
        R[r1] = 0  # case of underflow
        R["111"] = 8  # Raise OVERFLOW flag
        dump()
    else:
        resetFlag()
        dump()


def lShift(r1, imm):
    R[r1] = R[r1] << imm
    if R[r1] > 65535:
        R[r1] = R[r1] % 65535
        R["111"] = 8
        dump()
    else:
        resetFlag()
        dump()


def xor(r1, r2, r3):
    R[r1] = R[r2] ^ R[r3]
    if R[r1] > 65535:
        R[r1] = R[r1] % 65535
        R["111"] = 8  # Raise OVERFLOW flag
        dump()
    else:
        resetFlag()
        dump()


def AND(r1, r2, r3):
    R[r1] = R[r2] & R[r3]
    if R[r1] > 65535:
        R[r1] = R[r1] % 65535
        R["111"] = 8  # Raise OVERFLOW flag
        dump()
    else:
        resetFlag()
        dump()


def invert(reg1, reg2):
    R[reg1] = 65535 ^ R[reg2]
    resetFlag()
    dump()


def compare(r1, r2):
    resetFlag()
    if R[r1] == R[r2]:
        R["111"] = 1
    elif R[r1] > R[r2]:
        R["111"] = 2
    else:
        R["111"] = 4
    dump()


def load(r1, mem):
    R[r1] = binaryToInteger(memFile.mem[binaryToInteger(mem)])
    resetFlag()
    dump()


def store(r1, mem):
    memFile.mem[binaryToInteger(mem)] = integerToBinary(R[r1], 16)
    resetFlag()
    dump()


def jmp(mem):
    resetFlag()
    dump()
    global PC
    PC = binaryToInteger(mem)


def jgt(line):
    global PC
    if R["111"] == 2:
        resetFlag()
        dump()
        PC = binaryToInteger(line)
    else:
        resetFlag()
        dump()
        PC += 1


def addf(r1, r2, r3):
    # add floating point r2 and r3 and store in r1
    R[r1] = floatToDec(R[r2]) + floatToDec(R[r3])
    if R[r1] > 252.0:
        R[r1] = 252.0
        R["111"] = 8
        dump()
    else:
        resetFlag()
        dump()


def subf(r1, r2, r3):
    # subtract floating point r2 and r3 and store in r1
    R[r1] = floatToDec(R[r2]) - floatToDec(R[r3])
    if R[r1] < 0:
        R[r1] = 0
        R["111"] = 8
        dump()
    else:
        resetFlag()
        dump()


def movf(r1, imm):
    R[r1] = floatToDec(imm)
    resetFlag()
    dump()


def je(line):
    global PC
    if R["111"] == 1:
        resetFlag()
        dump()
        PC = binaryToInteger(line)
    else:
        resetFlag()
        dump()
        PC += 1


def jlt(line):
    global PC
    if R["111"] == 4:
        resetFlag()
        dump()
        PC = binaryToInteger(line)
    else:
        resetFlag()
        dump()
        PC += 1


def dump():
    print(integerToBinary(int(PC), 7), end=" ")
    for reg in R:
        print(integerToBinary(int(R[reg]), 16), end=" ")
    print()


lines = []

count = 0
while hltFlag != 1:
    count += 1
    if count > 100000:
        break
    Cycle += 1
    line = memFile.getInst(PC)
    opcode = line[0:5]
    opcodeType = findOpcodeType(opcode)

    if opcodeType == "A":
        reg1 = line[7:10].strip()
        reg2 = line[10:13].strip()
        reg3 = line[13:].strip()

        if opcode == "10000":
            add(reg1, reg2, reg3)
            PC += 1

        elif opcode == "10001":
            sub(reg1, reg2, reg3)
            PC += 1

        elif opcode == "10110":
            mul(reg1, reg2, reg3)
            PC += 1

        elif opcode == "11010":
            xor(reg1, reg2, reg3)
            PC += 1

        elif opcode == "11011":
            OR(reg1, reg2, reg3)
            PC += 1

        elif opcode == "11100":
            AND(reg1, reg2, reg3)
            PC += 1

        elif opcode == "10001":
            sub(reg1, reg2, reg3)
            PC += 1

        elif opcode == "00000":
            addf(reg1, reg2, reg3)

        elif opcode == "00001":
            subf(reg1, reg2, reg3)

    elif opcodeType == "B":
        reg1 = line[5:8].strip()
        imm1 = line[8:].strip()
        imm = binaryToInteger(line[8:].strip())

        if opcode == "10010":
            movImm(reg1, imm)
            PC += 1

        elif opcode == "11001":
            lShift(reg1, imm)
            PC += 1

        elif opcode == "11000":
            rShift(reg1, imm)
            PC += 1

        elif opcode == "10111":
            movf(reg1, imm1)

    elif opcodeType == "C":
        reg1 = line[10:13].strip()
        reg2 = line[13:].strip()

        if opcode == "10011":
            movReg(reg1, reg2)
            PC += 1

        elif opcode == "10111":
            divide(reg1, reg2)
            PC += 1

        elif opcode == "11101":
            invert(reg1, reg2)
            PC += 1

        elif opcode == "11110":
            compare(reg1, reg2)
            PC += 1

    elif opcodeType == "D":
        reg1 = line[5:8].strip()
        memAddr = line[8:].strip()

        if opcode == "10100":
            load(reg1, memAddr)
            PC += 1

        elif opcode == "10101":
            store(reg1, memAddr)
            PC += 1

    elif opcodeType == "E":
        memAddr = line[8:].strip()

        if opcode == "11111":
            jmp(memAddr)

        elif opcode == "01100":
            jlt(memAddr)

        elif opcode == "01101":
            jgt(memAddr)

        elif opcode == "01111":
            je(memAddr)

    elif opcodeType == "F":
        hltFlag = 1
        dump()
        break


memFile.dump()