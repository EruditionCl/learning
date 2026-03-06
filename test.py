
import math
counter=0

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
        if not any(isinstance(value, type) for type in (float,int)):
            raise ValueError("Constant only accepts float or int")
        self.value=value

    def diff(self,variable):
        return Constant(0)
    
    def simplified(self):
        return self
    
    def __str__(self):
        return f"{self.value}"
    
    def __eq__(self,other):
        return isinstance(other,Constant) and self.value==other.value
    
    def __add__(self,other):
        return self.value+other.value
    
    def __sub__(self,other):
        return self.value-other.value

    def __mul__(self,other):
        if isinstance(other, int) or isinstance(other,float):
            return Constant(self.value*other)
        return self.value*other.value
    
    def __rmul__(self,other):
        return self.__mul__(other)
    
    def __truediv__(self,other):
        return self.value/other.value
    
    def __pow__(self,other):
        return pow(self.value,other.value)
    
    
class Variable(Value):
    def __init__(self,symbol):
        self.symbol=symbol

    def diff(self,variable):
        if variable==self.symbol:
            return Constant(1)
        
    def __str__(self):
        return f"{self.symbol}"
        
class Add(Function):
    def __new__(cls,x,y):

        obj = super().__new__(cls)
        obj.x=x
        obj.y=y
        return obj.simplified()

    def __init__(self,x,y):
        self.x=x
        self.y=y

    def diff(self,variable):
        return Add(self.x.diff(variable),self.y.diff(variable))
    
    def __str__(self):
        return f"{self.x}+{self.y}"
    
    def simplified(self):
        if self.x==Constant(0):
            return self.y
        elif self.y==Constant(0):
            return self.x
        if self.x==self.y:
            return Multiply(2,self.x)
        if all(isinstance(expr,Constant) for expr in (self.x,self.y)):
            return Constant(self.x+self.y)
        return self
    
class Substract(Function):
    def __new__(cls,x,y):

        obj = super().__new__(cls)
        obj.x=x
        obj.y=y
        return obj.simplified()

    def __init__(self,x,y):
        self.x=x
        self.y=y

    def diff(self,variable):
        return Substract(self.x.diff(variable),self.y.diff(variable))
    
    def simplified(self):
        if self.y==Constant(0):
            return self.x
        if self.x==self.y:
            return Constant(0)
        if all(isinstance(expr,Constant) for expr in (self.x,self.y)):
            return Constant(self.x-self.y)
        return self
    
    def __str__(self):
        return f"{self.x}-{self.y}"

class Multiply(Function):
    def __new__(cls,x,y):
        obj = super().__new__(cls)
        obj.x=x
        obj.y=y
        return obj.simplified()

    def __init__(self,x,y):
        self.x=x
        self.y=y

    def diff(self,variable):
        return Add(Multiply(self.x,self.y.diff(variable)),
                   Multiply(self.x.diff(variable),self.y))
    
    def __str__(self):
        return f"{self.x}*{self.y}"
    
    def simplified(self):
        if any(value==Constant(0) for value in (self.x,self.y)):
            return Constant(0)
        if self.x==Constant(1):
            return self.y
        elif self.y==Constant(1):
            return self.x
        if all(isinstance(expr,Constant) for expr in (self.x,self.y)):
            return Constant(self.x*self.y)
        if self.x==self.y:
            return Power(self.x,2)
        return self

class Divide(Function):
    def __new__(cls,x,y):
        obj = super().__new__(cls)
        obj.x=x
        obj.y=y
        return obj.simplified()

    def __init__(self,x,y):
        self.x=x
        self.y=y

    def diff(self,variable):
        return Divide(Substract(Multiply(self.y,self.x.diff(variable)),
                   Multiply(self.y.diff(variable),self.x)),
                   Multiply(self.y,self.y))
    
    def simplified(self):
        if self.y==Constant(0):
            raise ZeroDivisionError("self.y can't be Constant(0)")
        if self.x==Constant(0):
            return Constant(0)
        if self.x==Constant(1):
            return Power(self.y,-1)
        if self.y==Constant(1):
            return self.x
        if all(isinstance(expr,Constant) for expr in (self.x,self.y)):
            return Constant(self.x/self.y)
        if self.x==self.y:
            return Constant(1)
        return self
    
    def __str__(self):
        return f"{self.x}/{self.y}"
    
class Power(Function):
    def __new__(cls,x,exponent):
        obj = super().__new__(cls)
        obj.x=x
        obj.exponent=exponent
        return obj.simplified()

    def __init__(self,x,exponent):
        self.x=x
        self.exponent=exponent

    def simplified(self):
        if all(isinstance(value,Constant) for value in (self.x,self.exponent)):
            return Constant(pow(self.x,self.exponent))
        if self.exponent==Constant(0):
            return Constant(1)
        if self.exponent==Constant(1):
            return self.x
        return self
    
    def __str__(self):
        if isinstance(self.x,Function) and isinstance(self.exponent,Function):   
            return f"({self.x}) ^ ({self.exponent})"    
        if isinstance(self.x,Function):
            return f"({self.x}) ^ {self.exponent}"
        if isinstance(self.exponent,Function):
            return f"{self.x} ^ ({self.exponent})"
        else:
            return f"{self.x} ^ {self.exponent}"
        
x=Variable("x")
y=Multiply(x,x)
z=Multiply(y,x)
print(z)
