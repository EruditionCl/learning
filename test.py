
import math

counter=0

def setconstant(x,y): 
    if isinstance(y, (int, float)):
            y = Constant(y)
    if isinstance(x, (int, float)):
            x = Constant(x)
    return x,y

class Expression: 
    def __init__(self):
        pass

class Value(Expression): 
    def __init__(self):
        pass

class Function(Expression):
    def __init__(self):
        pass

    def express(self,x): 
        if isinstance(self.x,Function):
            return self.x.express(x)
        if isinstance(self.y,Function):
            return self.y.express(x)
        if isinstance(self.x,Variable):
            return type(self)(x,self.y)
        if isinstance(self.y,Variable):
            return type(self)(self.x,x)
        if isinstance(self.x,Variable) and isinstance(self.y,Variable):
            return type(self)(x,x)

class Constant(Value):
    def __init__(self,value):
        if isinstance(value,Constant):
            value=value.value

        if not any(isinstance(value, type) for type in (float,int)):
            raise ValueError("Constant only accepts float or int")
        self.value=value

    def diff(self,variable):
        return Constant(0)
    
    def simplified(self):
        return self
    
    def express(self, x):
        return self
    
    def degree(self):
        return 0
    
    def __str__(self):
        return f"{self.value}"
    
    def __eq__(self,other):
        return isinstance(other,Constant) and self.value==other.value
    
    def __add__(self,other):
        if isinstance(other,(int,float)):
            return Constant(self.value+other)
        return Constant(self.value+other.value)
    
    def __sub__(self,other):
        if isinstance(other,(int,float)):
            return Constant(self.value-other)
        return Constant(self.value-other.value)

    def __mul__(self,other):
        if isinstance(other, int) or isinstance(other,float):
            return Constant(self.value*other)
        return Constant(self.value*other.value)
    
    def __rmul__(self,other):
        return self.__mul__(other)
    
    def __truediv__(self,other):
        if isinstance(other,(int,float)):
            return Constant(self.value/other)
        return Constant(self.value/other.value)
    
    def __pow__(self,other):
        if isinstance(other,(int,float)):
            return Constant(pow(self.value,other))
        return Constant(pow(self.value,other.value))
    
    def __gt__(self,other):
        if isinstance(other,(int,float)):
            return self.value>other
        return self.value>other.value
    
    def __lt__(self,other):
        if isinstance(other,(int,float)):
            return self.value<other
        return self.value<other.value
    
    
class Variable(Value):
    def __init__(self,symbol):
        self.symbol=symbol

    def diff(self,variable):
        if variable==self.symbol:
            return Constant(1)
        else:
            return Constant(0)

    def degree(self):
        return 1
        
    def __str__(self):
        return f"{self.symbol}"

x=Variable("x") # Easy to just store it here instead of typing it manually for every test

class Add(Function):
    def __new__(cls,x,y):
        x,y=setconstant(x,y)
        obj = super().__new__(cls)
        obj.x=x
        obj.y=y
        return obj.simplified()

    def __init__(self,x,y):
        pass

    def diff(self,variable):
        return Add(self.x.diff(variable),self.y.diff(variable))
    
    def __str__(self):
        left=f"{self.x}"
        right=f"{self.y}"
        if any(isinstance(self.x,function) for function in (Divide,Power)):
            left=f"({self.x})"
        if any(isinstance(self.y,function) for function in (Divide,Power)):
            right=f"({self.y})"
        return f"{left}+{right}"
    
    def simplified(self):
        if self.x == Constant(0): return self.y
        if self.y == Constant(0): return self.x
        if self.x==self.y: return Multiply(2,self.x)
        if all(isinstance(expr,Constant) for expr in (self.x,self.y)): 
            return Constant(self.x+self.y)
        if isinstance(self.x, Constant) and not isinstance(self.y, Constant):
            return Add(self.y, self.x)
        if isinstance(self.x, Add):
            return Add(self.x.x, Add(self.x.y, self.y))
        if isinstance(self.x, Multiply) and isinstance(self.y, Multiply):
            if self.x.y == self.y.y:
                return Multiply( Add(self.x.x, self.y.x), self.x.y )
        if isinstance(self.x, Multiply) and isinstance(self.y, Add):
            if isinstance(self.y.x, Multiply): 
                if self.x.y == self.y.x.y:
                    return Add(Multiply(Add(self.x.x, self.y.x.x),self.x.y), self.y.y)
        return self

        
    def degree(self):
        return max(self.x.degree(),self.y.degree())
    
class Substract(Function):
    def __new__(cls,x,y):
        x,y=setconstant(x,y)
        obj = super().__new__(cls)
        obj.x=x
        obj.y=y
        return obj.simplified()

    def __init__(self,x,y):
        pass

    def diff(self,variable):
        return Substract(self.x.diff(variable),self.y.diff(variable))
    
    def simplified(self):
        if self.y==Constant(0):
            return self.x
        if self.x==self.y:
            return Constant(0)
        if all(isinstance(expr,Constant) for expr in (self.x,self.y)):
            return Constant(self.x-self.y)
        if isinstance(self.x, Substract):
            return Substract(self.x.x,Add(self.x.y,self.y))
        if isinstance(self.y, Substract):
            return Substract(self.y.x,Add(self.y.y,self.x))
        return self
    
    def __str__(self):
        left=f"{self.x}"
        right=f"{self.y}"
        if all(isinstance(expr,(Power,Divide)) for expr in (self.x,self.y)):
            left=f"({self.x})"
            right=f"({self.y})"
        if isinstance(self.x,(Power,Divide)):
            left=f"({self.x})" 
        if isinstance(self.y,(Power,Divide,Add,Substract)):
            right=f"({self.y})"

        return f"{left}-{right}"
    
    def degree(self):
        return max(self.x.degree(),self.y.degree())

class Multiply(Function):
    def __new__(cls,x,y):
        x,y=setconstant(x,y)
        obj = super().__new__(cls)
        obj.x=x
        obj.y=y
        return obj.simplified()

    def __init__(self,x,y):
        pass

    def diff(self,variable):
        return Add(Multiply(self.x,self.y.diff(variable)),
                   Multiply(self.x.diff(variable),self.y))
    
    def __str__(self):
        if isinstance(self.x,Function) and isinstance(self.y,Function):
            return f"({self.x})({self.y})"
        if isinstance(self.x,Function) and isinstance(self.y,Constant):
            return f"{self.y}({self.x})"
        if isinstance(self.y,Function) and isinstance(self.x,Constant):
            return f"{self.x}({self.y})"
        if isinstance(self.x,Constant):
            return f"{self.x}{self.y}"
        if isinstance(self.y,Constant):
            return f"{self.y}{self.x}" 
    
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
        if isinstance(self.x,Power):
            if self.x.x==self.y:
                return Power(self.x.x,self.x.y+1)
        if isinstance(self.y,Power):
            if self.y.x==self.x:
                return Power(self.y.x,self.y.y+1)
        if isinstance(self.x,Power) and isinstance(self.y,Power):
            if self.x.x==self.y.x:
                return Power(self.x.x, self.x.y+self.y.y)
        if isinstance(self.x,Multiply):
            return Multiply(self.x.x,Multiply(self.x.y,self.y))
        if isinstance(self.y,Multiply):
            return Multiply(self.y.x,Multiply(self.y.y,self.x))
        if isinstance(self.y,Constant) and not isinstance(self.x,Constant):
            return Multiply(self.y,self.x)
        if any(isinstance(self.y,function) for function in (Add,Substract,Divide)):
            if isinstance(self.x, Value):
                return type(self.y)(Multiply(self.x,self.y.x),Multiply(self.x,self.y.y))
            elif any(isinstance(self.x,function) for function in (Add,Substract,Divide)):
                return Add(Add(Multiply(self.x.x,self.y.x),Multiply(self.x.x,self.y.y)),Add(Multiply(self.x.y,self.y.x),Multiply(self.x.y,self.y.y)))
        if any(isinstance(self.x,function) for function in (Add,Substract,Divide)):
            if isinstance(self.y, Value):
                return type(self.x)(Multiply(self.y,self.x.x),Multiply(self.y,self.x.y))
            elif any(isinstance(self.y,function) for function in (Add,Substract,Divide)):
                return Add(Add(Multiply(self.x.x,self.y.x),Multiply(self.x.x,self.y.y)),Add(Multiply(self.x.y,self.y.x),Multiply(self.x.y,self.y.y)))
        return self
    
    def degree(self):
        return Constant(self.x.degree()) + Constant(self.y.degree())

class Divide(Function):
    def __new__(cls,x,y):
        x,y=setconstant(x,y)
        obj = super().__new__(cls)
        obj.x=x
        obj.y=y
        return obj.simplified()

    def __init__(self,x,y):
        pass

    def diff(self,variable):
        return Divide(Substract(Multiply(self.y,self.x.diff(variable)),
                   Multiply(self.y.diff(variable),self.x)),
                   Multiply(self.y,self.y))
    
    def simplified(self):
        if isinstance(self.y, Constant) and not isinstance(self.x, Constant):
            return Multiply(self.y, self.x)
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
        if isinstance(self.x,Power):
            if self.x.x==self.y:
                return Power(self.x.x,self.x.y-Constant(1))
        if isinstance(self.y,Power):
            if self.y.x==self.x:
                return Power(self.y.x,Constant(1)-self.y.y)
        if isinstance(self.x,Power) and isinstance(self.y,Power):
            if self.x.x==self.y.x:
                return Power(self.x.x, self.x.y-self.y.y)
        if isinstance(self.x,Divide):
            return Divide(self.x.x,Multiply(self.x.y,self.y))
        if isinstance(self.y,Divide):
            return Divide(Multiply(self.x,self.y.y),self.y.x)        
        return self
    
    def __str__(self):
        left=f"{self.x}"
        right=f"{self.y}"
        if any(isinstance(self.x,function) for function in (Add,Substract,Divide,Power)):
            left=f"({self.x})"
        if any(isinstance(self.y,function) for function in (Add,Substract,Divide,Power)):
            right=f"({self.y})"
        return f"{left}/{right}"

    def degree(self):
        return max(self.x.degree(),self.y.degree())
    
class Power(Function):
    def __new__(cls,x,y):
        x,y=setconstant(x,y)
        obj = super().__new__(cls)
        obj.x=x
        obj.y=y
        return obj.simplified()

    def __init__(self,x,y):
        pass

    def simplified(self):
        if all(isinstance(value,Constant) for value in (self.x,self.y)):
            return pow(self.x,self.y)
        if self.y==Constant(0):
            return Constant(1)
        if self.y==Constant(1):
            return self.x
        if isinstance(self.x,Power):
            return Power(self.x.x,self.x.y*self.y)
        if isinstance(self.x,Constant) and not isinstance(self.y,Constant):
            return Power(self.y,self.x)
        return self
    
    def diff(self,variable):
        return Multiply(self.y, Power(self.x,self.y-1))
    
    def __str__(self):
        if isinstance(self.x,Function) and isinstance(self.y,Function):   
            return f"({self.x}) ^ ({self.y})"    
        if isinstance(self.x,Function):
            return f"({self.x}) ^ {self.y}"
        if isinstance(self.y,Function):
            return f"{self.x} ^ ({self.y})"
        return f"{self.x} ^ {self.y}"
    
    def degree(self):
        if isinstance(self.y, Constant):
            return self.x.degree() * self.y.value
        return 0 
        
a=Power(x,2)
b=Add(a,3)
print(a.express(5))