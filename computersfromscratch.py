
def boolchecker(func):
    def inner(*args,**kwargs):
        values=list(args)
        values.extend(kwargs.values())
        for value in values:
            if isinstance(value,bool):
                if value==True:
                    value=1
                if value==False:
                    value==0
            if value==0 or value==1:
                pass
            else:
                raise TypeError("Inputs must be bool or 0 or 1")
        return func(*args,**kwargs)
    return inner
        

@boolchecker
def NAND(a,b):
    if 0 in (a,b):
        return 1
    else:
        return 0

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

def Add(a,b):
    if not isinstance(a,list) or not isinstance(b,list):
        raise TypeError("Add accepts only lists of 0 and 1")
    
    def normalizebit(bit):
        if bit in (True,1):
            return 1
        elif bit in (False,0):
            return 0
        else:
            raise ValueError("bit must be bool, 0 or 1")
    
    a=[normalizebit(bit) for bit in a]
    b=[normalizebit(bit) for bit in b]

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


    

