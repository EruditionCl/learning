
from decorators import *

@boolchecker
def NAND(a,b):
    if 0 in (a,b):
        return 1
    else:
        return 0

@gatelist
@boolchecker
def NOT(a):
    return NAND(a,a)

@boolchecker
def AND(a,b):
    return NOT(NAND(a,b))

@boolchecker
def OR(a,b):
    return NOT(AND(NOT(a),NOT(b)))

@boolchecker
def XOR(a,b):
    return AND(OR(a,b),NAND(a,b)) 

@boolchecker
def HalfAdder(a,b):
    return XOR(a,b),AND(a,b)

@boolchecker
def FullAdder(a,b,c):
    return XOR(XOR(a,b),c), OR((OR(AND(a,b),AND(b,c))),AND(a,c))

@listchecker
def Add(a,b):

    if len(a)!=len(b):
        diff = abs(len(a)-len(b))
        if len(a)>len(b):
            b = diff * [0] + b
        else:
            a = diff * [0] + a

    a=a[::-1]
    b=b[::-1]
    final = []
    carry=0

    for i in range(len(a)):
        o,carry = FullAdder(a[i],b[i],carry)
        final.append(o)
    final.append(carry)
    return final[::-1]   

@listchecker
@bit16
def Add16(a,b):
    return Add(a,b)

@listchecker
@bit16
def ALU(a,b,zx,nx,zy,ny,f,no):
    pass

a=[1,0,1]
print(NOT(a))
