#!/usr/bin/env python
from inspect import getargspec
from sys import stdout
from time import sleep


def argNumber(method):
    (args, _, _, _) = getargspec(method)
    return len(args)


def readReg(reg):
    reg = reg - 32768
    try:
        return registers[reg]
    except IndexError:
        print "%d :invalid register on reading operation" % reg

def writeReg(reg, value):
    global pc
    reg = reg - 32768
    try:
        registers[reg] = value
        if value > 32767:
            print "%d : Writing %d in register %d" % (pc, value, reg)
            sleep(1)
    except IndexError:
        print "%d :invalid register on writing operation" % reg
    if reg == 7:
        print "I JUST WROTE TO THE MAGIC EIGHTH REGISTER"


def log(string):
    global _LOG_
    if _LOG_ and True:
        _LENGTH_ = 40

        # Getting registers in a nice $0...$7 display
        #could be done in a simpler way by the calling functions, but this feature was an afterthought... after writing all the function calls
        toLog = string.split(" ")
        for word in toLog:
            try:
                if int(word) > 32767:
                    string = string.replace(word, "$%d" % (int(word) - 32768), 1)
            except ValueError:
                pass
        ###
        string = string.split("!!!")
        string[0] += " " * ((_LENGTH_ - len(string[0])) if len(string[0]) < _LENGTH_ else 0) # alignment padding. There's probably already
        string[1] += " " * ((_LENGTH_ - len(string[1])) if len(string[1]) < _LENGTH_ else 0) #some function for this.
        string = string[0] + string[1] + "%s" % registers
        file = open("log.txt", "a")
        file.write(string+"\n")
        file.close()



### Functions used by the virtual machine:

def halt():
    global stop
    stop = True
    global pc
    log("%s:  halt     !!!halt   " % pc)

def set(a, b):
    if b > 32767: #b is a register
        value = readReg(b)
    else:
        value = b
    writeReg(a, value)
    global pc
    pc += 3 #function name + 2 arguments
    log("%s:  set %d %d    !!!set %d %d" % (pc, a, b, a, value))


def push(a):
    if a > 32767:
        value = readReg(a)
    else:
        value = a
    stack.append(value)
    global pc
    log("%s:  push %d    !!!push %d" % (pc, a, value))
    pc += 2


def pop(a):
    value = stack.pop()
    writeReg(a, value)
    global pc
    log("%s:  pop %d    !!!pop %d <- %d" % (pc, a, a, value))
    pc += 2


def eq(a, b, c):
    if b > 32767:
        left = readReg(b)
    else:
        left = b

    if c > 32767:
        right = readReg(c)
    else:
        right = c

    writeReg(a, 1) if left == right else writeReg(a, 0)
    global pc
    log("%s:  eq %d %d %d      !!!eq %d %d %d" % (pc, a, b, c, a, left, right))
    pc += 4    


def gt(a,b,c):
    if b > 32767:
        left = readReg(b)
    else:
        left = b

    if c > 32767:
        right = readReg(c)
    else:
        right = c

    writeReg(a, 1) if left > right else writeReg(a, 0)
    global pc
    log("%s:  gt %d %d %d      !!!gt %d %d %d" % (pc, a, b, c, a, left, right))
    pc += 4


def jmp(a):
    if a > 32767:
        address = readReg(a)
    else:
        address = a
    global pc
    log("%s:  jmp %d    !!!jmp %d" % (pc, a, address))
    pc = address


def jt(a, b):
    if a > 32767:
        check = readReg(a)
    else:
        check = a

    global pc
    log("%s:  jt %d %d       !!!jt %d %d" % (pc, a, b, check, readReg(b) if b > 32767 else b))
    pc += 3

    if not check == 0:
        if b > 32767:
            address = readReg(b)
        else:
            address = b
        pc = address


def jf(a, b):
    if a > 32767:
        check = readReg(a)
    else:
        check = a
    global pc
    log("%s:  jf %d %d       !!!jf %d %d" % (pc, a, b, check, readReg(b) if b > 32767 else b))
    pc += 3

    if check == 0:
        if b > 32767:
            address = readReg(b)
        else:
            address = b
        pc = address




def add(a, b, c):
    if b > 32767:
        left = readReg(b)
    else:
        left = b

    if c > 32767:
        right = readReg(c)
    else:
        right = c
    writeReg(a, (left+right) % 32768)
    global pc
    log("%s:  add %d %d %d      !!!add %d %d %d" % (pc, a, b, c, a, left, right))
    pc += 4


def mult(a, b, c):
    if b > 32767:
        left = readReg(b)
    else:
        left = b

    if c > 32767:
        right = readReg(c)
    else:
        right = c
    writeReg(a, (left*right) % 32768)

    global pc
    log("%s:  mult %d %d %d      !!!mult %d %d %d" % (pc, a, b, c, a, left, right))
    pc += 4


def mod(a, b, c):
    if b > 32767:
        left = readReg(b)
    else:
        left = b

    if c > 32767:
        right = readReg(c)
    else:
        right = c
    writeReg(a, left % right)
    global pc
    log("%s:  mod %d %d %d      !!!mod %d %d %d" % (pc, a, b, c, a, left, right))
    pc += 4


def logAnd(a, b, c):
    if b > 32767:
        left = readReg(b)
    else:
        left = b

    if c > 32767:
        right = readReg(c)
    else:
        right = c
    writeReg(a, left & right)
    global pc
    log("%s:  and %d %d %d      !!!and %d %d %d" % (pc, a, b, c, a, left, right))
    pc += 4


def logOr(a, b, c):
    if b > 32767:
        left = readReg(b)
    else:
        left = b

    if c > 32767:
        right = readReg(c)
    else:
        right = c
    writeReg(a, left | right)
    global pc
    log("%s:  or %d %d %d      !!!or %d %d %d" % (pc, a, b, c, a, left, right))
    pc += 4


def logNot(a, b):
    if b > 32767:
        value = readReg(b)
    else:
        value = b
    value = (~value) & 32767 #reverses and then erases bits after the 15th
    writeReg(a, value)
    global pc
    log("%s:  not %d %d       !!!not %d %d" % (pc, a, b, a, value))
    pc += 3


def rmem(a, b):
    if b > 32767:
        address = readReg(b)
    else:
        address = b
    writeReg(a, memory[address])
    global pc
    log("%s:  rmem %d %d      !!!rmem %d %d <-- %d" % (pc, a, b, a, address, memory[address]))
    pc += 3


def wmem(a, b):
    if a > 32767:
        address = readReg(a)
    else:
        address = a

    if b > 32767:
        value = readReg(b)
    else:
        value = b
#    print "wmem %d %d" % (a, b)
#    print "%s ->" % memory[address-5:address+5],

    memory[address] = value

#    print memory[address-5:address+5]
#    print registers
    global pc
    log("%s:  wmem %d %d      !!!wmem %d %d" % (pc, a, b, address, value))
    pc += 3


def call(a):
    global pc
#    pc += 2
    stack.append(pc+2) # put address of next instruction in stack
    if a > 32767:
        address = readReg(a)
    else:
        address = a
    log("%s:  call %d    !!!call %d" % (pc, a, address))
    jmp(address) #changes pc


def ret():
    try:
        address = stack.pop()
        jmp(address)
    except IndexError: #stack empty
        halt()
    log("%s:  ret    !!!ret" % pc)
    

def out(a):
    if a > 32767:
        ascii = readReg(a)
    else:
        ascii = a
#    print chr(ascii),  #adds a space between each printed character; Purely for retro visual
    stdout.write(chr(ascii))
    global pc
    log("%s:  out %d    !!!out %r" % (pc, a, chr(ascii)))
    pc += 2

buffer = open("gameInput.txt").read()
bufferIndex = 0

def cIn(a):
    global buffer
    global bufferIndex
    if not bufferIndex < len(buffer):
        buffer = raw_input()
        buffer += "\n"
        bufferIndex = 0
        global _LOG_
        _LOG_ = True #start logging after the instructions in the text file are over
#    print "Buffer = %r , Index = %d" % (buffer, bufferIndex)
    writeReg(a, ord(buffer[bufferIndex]))
    bufferIndex += 1
    global pc
    log("%s:  in %d    !!!in %d -> %r" % (pc, a, ord(buffer[bufferIndex-1]), buffer[bufferIndex-1] ))
    pc += 2

def noop():
    global pc
    pc += 1


functions = [halt, set, push, pop, eq, gt, jmp, jt, jf, add, mult, mod, logAnd, logOr, logNot, rmem, wmem, call, ret, out, cIn, noop]
#each functions is called with function[opcode](arguments)


registers = [0, 0, 0, 0, 0, 0, 0, 2] #8 registers, 0 through 7

stack = [] # can grow (virtually) unbounded

memory = [0] * 32768 #15-bit addresses 0...32767

_LOG_ = False

### Loading program into memory:

#input = open("challenge.bin", "rb")
input = open("challenge.bin")
index = 0
while True:
    low = input.read(1)
    if low == "":  # program comes in pairs (low, high), so the file won't end between a low and an high
        break
    high = input.read(1)
    complete = (ord(high) << 8) | ord(low)
    memory[index] = complete
    index += 1
input.close()


#################
memory[521] = 8 #this changes jt EIGHT_REGISTER ERROR_SECTION to a jf, allowing the eighth register to start as not zero
#memory[5495] = 7 #similar to the above (jf -> jt). hopefully, it will stop detection of incorrect calibration
memory[6027] = 18 # ret. A call to 6027 starts an endless(?) loop of calls to itself and stack pushs and pops. let's see what happens if it just returns
#################

stop = False #both of these are changed by the functions
pc = 0 #program counter 

while not stop:
    if pc >= len(memory):
        break
    try:
        number = argNumber(functions[memory[pc]])
    except IndexError:
        print "Index Error: PC = %d, opcode = %d" % (pc, memory[pc])
    if number == 0:
        functions[memory[pc]]()
    elif number == 1:
        functions[memory[pc]](memory[pc+1])
    elif number == 2:
        functions[memory[pc]](memory[pc+1], memory[pc+2])
    elif number == 3:
        functions[memory[pc]](memory[pc+1], memory[pc+2], memory[pc+3])
    #keep going if functions are added with more than 3 arguments

#    print stack,
#    print registers    


#for i in range(len(functions)):
#    print "%s : %d" % (functions[i].__name__ , i)


""" Write program to human-readable file
file = open("program.txt", "w")
index = 0
while index < len(memory):
    try:
        file.write("%d    %s" % (index, functions[memory[index]].__name__))
        number = argNumber(functions[memory[index]])
        if number == 0:
            index += 1
        elif number == 1:
            file.write(" %s" % memory[index+1])
            index += 2
        elif number == 2:
            file.write(" %s %s" % (memory[index+1], memory[index+2]))
            index += 3
        elif number == 3:
            file.write(" %s %s %s" % (memory[index+1], memory[index+2], memory[index+3]))
            index += 4
    except IndexError:
        print "Index Error: PC = %d, opcode = %d" % (index, memory[index])
        file.write("%d    %s" % (index, memory[index]))
        index += 1
    file.write("\n")

file.close()

"""

#for i in range(10):
#    print "%d : %d" % (i+838, memory[i+838])
#print len(memory)
