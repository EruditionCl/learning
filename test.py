
class Expression:
    def __init__(self):
        pass

class Value(Expression):
    def __init__(self):
        pass

class Function(Expression):
    def __init__(self):
        pass

expressions=[Value,Function]

class Constant(Value):
    def __init__(self,value):
        self.value=value

    def diff(self,variable):
        return Constant("0")
    
    def __str__(self):
        return f"{self.value}"
    
class Variable(Value):
    def __init__(self,symbol):
        self.symbol=symbol

    def diff(self,variable):
        if variable==self.symbol:
            return Constant(1)
        
    def __str__(self):
        return f"{self.symbol}"
        
class Add(Function):
    def __init__(self,x,y):
        for expression in expressions:
            pass
        self.x=x
        self.y=y

    def diff(self,variable):
        return Add(self.x.diff(variable),self.y.diff(variable))
    
    def __str__(self):
        return f"{self.x}+{self.y}"
    
class Substract(Function):
    def __init__(self,x,y):
        for expression in expressions:
            pass
        self.x=x
        self.y=y

    def diff(self,variable):
        return Substract(self.x.diff(variable),self.y.diff(variable))
    
    def __str__(self):
        return f"{self.x}-{self.y}"

class Multiply(Function):
    def __init__(self,x,y):
        for expression in expressions:
            pass
        self.x=x
        self.y=y

    def diff(self,variable):
        return Add(Multiply(self.x,self.y.diff(variable)),
                   Multiply(self.x.diff(variable),self.y))
    
    def __str__(self):
        return f"{self.x}*{self.y}"

class Divide(Function):
    def __init__(self,x,y):
        for expression in expressions:
            pass
        self.x=x
        self.y=y

    def diff(self,variable):
        return Divide(Substract(Multiply(self.x,self.y.diff(variable)),
                   Multiply(self.x.diff(variable),self.y)),
                   Multiply(self.y,self.y))
    
    def __str__(self):
        return f"{self.x}/{self.y}"

a=Constant(3)
b=Variable("x")
d=Multiply(b,b)
c=Divide(d,a)
print(c.diff("x"))
