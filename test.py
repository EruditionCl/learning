
import math

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

class Constant(Value):
    def __init__(self,value):
        if isinstance(value,Constant):
            value=value.value

        if not any(isinstance(value, type) for type in (float,int)):
            raise ValueError("Constant only accepts float or int")
        self.value=value
        self.symbolic=False

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
    
    def __eq__(self, other):
        if isinstance(other, Constant):
            return self.value == other.value
        if isinstance(other, (int, float)):
            return self.value == other
        return False
    
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
        if isinstance(other,Constant):
            return Constant(self.value*other.value)
        return Multiply(self, other)
    
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

class Symbol(Constant):
    def __init__(self):
        self.symbolic=True

    def __eq__(self,other):
        return isinstance(other,type(self))
    
    def __add__(self,other):
        return Add(self,other)
    
    def __radd__(self,other):
        return Add(other,self)

    def __sub__(self,other):
        return Substract(self,other)
    
    def __rsub__(self,other):
        return Substract(other,self)

    def __mul__(self,other):
        return Multiply(self,other)
    
    def __rmul__(self,other):
        return Multiply(other,self)
    
    def __truediv__(self,other):
        return Divide(self,other)
    
    def __rtruediv__(self,other):
        return Divide(other,self)
    
    def __pow__(self,other):
        return Power(self,other)
    
    def __gt__(self,other):
        if isinstance(other,(int,float)):
            return self.value>other
        return self.value>other.value
    
    def __lt__(self,other):
        if isinstance(other,(int,float)):
            return self.value<other
        return self.value<other.value
    
class Pi(Symbol):
    def __init__(self):
        self.value=3.14159265358979
        super().__init__()
    
    def __str__(self):
        return "π"
    
    
class Euler(Symbol):
    def __init__(self):
        self.value=2.718281828459045
        super().__init__()
    
    def __str__(self):
        return "e"
    
    
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

    def express(self, x):
        return Constant(x)
        
    def __str__(self):
        return f"{self.symbol}"

x=Variable("x") # Easy to just store it here instead of typing it manually for every test
y=Variable("y")
z=Variable("z")
valuetypes = (int, float)

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
        if isinstance(self.x,Power):
            left=f"({self.x})"
        if isinstance(self.y,Power):
            right=f"({self.y})"
        if isinstance(self.y,Constant) and self.y<0 or isinstance(self.y,Multiply) and self.y.x<0:
            return f"{left}{right}"
        return f"{left}+{right}"
    
    def simplified(self):
        if self.x == Constant(0): return self.y
        if self.y == Constant(0): return self.x
        if self.x==self.y: return Multiply(2,self.x)
        if all(isinstance(expr,Constant) for expr in (self.x,self.y)): 
            if self.x.symbolic==False and self.y.symbolic==False:
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
        return max(self.x,self.y)
    
    def express(self,x):
        return self.x.express(x)+self.y.express(x)


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
            if self.x.symbolic==False and self.y.symbolic==False:
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
        if isinstance(self.y,Constant) and not isinstance(self.x,Constant):
            return Multiply(self.y,self.x)
        if isinstance(self.x, Add):
            return Add(Multiply(self.x.x, self.y), Multiply(self.x.y, self.y))
        if isinstance(self.y, Add):
            return Add(Multiply(self.x, self.y.x), Multiply(self.x, self.y.y))
        return self
    
    def degree(self):
        return Constant(self.x.degree()) + Constant(self.y.degree())
    
    def express(self,x):
        return self.x.express(x)*self.y.express(x)

class Substract(Function):
    def __new__(cls,x,y):
        x,y=setconstant(x,y)
        return Add(x,Multiply(-1,y))

class Divide(Function):
    def __new__(cls,x,y):
        x,y=setconstant(x,y)
        return Multiply(x,Power(y,-1))
    
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
            if self.x.symbolic==False and self.y.symbolic==False:
                return pow(self.x,self.y)
        if self.y==Constant(0):
            return Constant(1)
        if self.y==Constant(1):
            return self.x
        if isinstance(self.x,Power):
            return Power(self.x.x,self.x.y*self.y)
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
        
    def express(self,x):
        return pow(self.x.express(x),self.y.express(x))
    
class Sin(Function):
    def __init__(self,angle):
        self.angle=angle

    def simplified(self):
        if isinstance(self.angle,Multiply):
            def is_integer_constant(val):
                return isinstance(val, Constant) and isinstance(val.value, int)
            if is_integer_constant(self.x.angle) and isinstance(self.y.angle,Pi):
                return Constant(0)
            if is_integer_constant(self.y.angle) and isinstance(self.x.angle,Pi):
                return Constant(0)
    

pi=Multiply(1,Pi())
print(Sin(pi).simplified())