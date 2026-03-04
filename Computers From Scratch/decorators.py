
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

def listchecker(func):
    def inner(a,b):
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
        return func(a,b)
    return inner

def bit16(func):
    def inner(a,b):
        sets=[a,b]

        for set in sets:
            diff = abs(len(set)-16)
            if len(set)<16:
                set[:] = diff*[0] + set
            elif len(set)>16:
                for _ in range(diff):
                    set.pop(0)
        return func(a,b)
    return inner

def gatelist(func):
    def inner (a):
        if not isinstance(a,list):
            pass
        else:
            for value in a:
                value=func(value)
                a[value]=value
            return a
    return inner
         