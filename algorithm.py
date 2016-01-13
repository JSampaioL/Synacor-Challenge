#!/usr/bin/env python
from time import sleep

#stack = []
#sp = 0 #stack pointer

a = 0
b = 0
c = 0
stackValue = 0


def trampoline():
    global a
    global b
    global c
    global stackValue
#    global sp
#    global stack
#    sp = 0
#    stack = [0] * 9000
    functions = [alg, help]
    todo = [] #as in todo list; holds the stack values to pass to the helper function
    code = 0 #function code
    while True:
        while True:
            
            (code, aux) = functions[code]()
            if code == 2:
                todo.append(aux) #help function and stackValue
                code = 0 #will run first function right after and the second when the first one "returns" (from a recursive perspective)
            if code < 0:
                break

#        print "Here; the stack has an astounding %d elements in it" % len(todo)
#        print todo
#        sleep(0.1)
        if todo: #defining here the help function
            b = a
            a = todo.pop()
            a -= 1
            code = 0
        else:
            break

    return a


"""s
#def help(a, b, c): #help doesn't need to get b, it instantly makes b = the first value; and it needs to get a value from the stack.
def help():
    global a
    global b
    global c
    global stackValue
    global sp
    b = a
    a = stackValue
#    a = stack.pop()

#    a = stack[sp]
#    sp -= 1

    a -= 1
    return (0, None)
"""



def alg():
    global a
    global b
    global c
    if a > 0:
        if b > 0:
            
#            stack.append(a)
 #           if len(stack) > 5000:
 #               print "HOLY COW! STACK LEN IS", len(stack)
            #global sp
            #sp += 1
            #stack[sp] = a

            b -= 1
            return (2, a) #this value of a must be stored and then passed to the help function
#            (a, b) = trampoline(a, b, c)
#            b = a
#            a = stack.pop()
#            a -= 1
#            return (0, a, b)

        elif b == 0:
            a -= 1
            b = c
            return (0, None)

        else:
            raise ValueError("$1 should not be negative: %d" % b)

    elif a == 0:
        a = b + 1
        return (-1, None) #Base value, no more function calls

    else:
        raise ValueError("$0 should not be negative: %d" % a)



"""d
### Attempt at understanding the algorithm
a = 4
b = 1
for c in range(1, 10):
    counter = 0
    while True:
        while a > 0:
            while b > 0:
                counter += 1
                stack.append(a)
                b -= 1
            a -= 1
            b = c
        a = b + 1
        b = a
        a = stack.pop()
        counter -= 1
#        print "Counter is %d" % counter
        if counter == 0:
            break
    print "%d : %s" % (c, (a, b))
"""




for i in range(1, 10):
    a = 4
    b = 1
    c = 1
    print "%d : %s" % (i, trampoline())



for i in xrange(32768):
    a = 4
    b = 1
    c = i
    result = trampoline()
    if result == 6:
        print "%d seems to work" % i
        break
    if i == 1:
        print "Got to the second! yay?", a, b, c
    if i % 10 == 0:
        print "Trying", i
