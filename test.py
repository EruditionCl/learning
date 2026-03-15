
import math as math

def setconstant(x,y): 
    if isinstance(y, (int, float)):y = Constant(y)
    if isinstance(x, (int, float)):x = Constant(x)
    return x,y

def s(): #delete later
    print("works")

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
    
    def express(self, x, var):
        return self
    
    def degree(self,var):
        return 0
    
    def has_variable(self,var):
        return False
    
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
    
    def __ge__(self,other):
        if isinstance(other,(int,float)):
            return self.value>=other
        return self.value>=other.value
    
    def __le__(self,other):
        if isinstance(other,(int,float)):
            return self.value<=other
        return self.value<=other.value
    
    def __mod__(self,other):
        if isinstance(other,(int,float)):
            return self.value%other
        return self.value%other.value

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
    
    
class Pi(Symbol):
    def __init__(self):
        self.value=math.pi
        super().__init__()
    
    def __str__(self):
        return "π"
    
    
class Euler(Symbol):
    def __init__(self):
        self.value=math.e
        super().__init__()
    
    def __str__(self):
        return "e"
    
    
class Variable(Value):
    def __init__(self,symbol):
        self.symbol=symbol

    def diff(self,variable):
        if variable==self:
            return Constant(1)
        else:
            return Constant(0)

    def degree(self,var):
        if self.symbol==var:
            return 1
        return 0

    def express(self, x, var):
        if var==self.symbol:
            return Constant(x)
        return self
    
    def has_variable(self,var):
        return self.symbol==var
        
    def __str__(self):
        return f"{self.symbol}"

x=Variable("x") # Easy to just store it here instead of typing it manually for every test
y=Variable("y")
z=Variable("z")
valuetypes = (Constant,int, float)

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

        
    def degree(self,var):
        return max(self.x.degree(var),self.y.degree(var))
    
    def express(self,x,var):
        return Add(self.x.express(x,var),self.y.express(x,var))

    def has_variable(self,var):
        return self.x.has_variable(var) or self.y.has_variable(var)

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
        if self.x==-1:
            return f"-{self.y}"
        if self.y==-1:
            return f"-{self.x}"
        if isinstance(self.x,Function) and isinstance(self.y,Function):
            return f"({self.x})({self.y})"
        if isinstance(self.x,Function) and isinstance(self.y,Value):
            return f"{self.y}({self.x})"
        if isinstance(self.y,Function) and isinstance(self.x,Value):
            return f"{self.x}({self.y})"
        if isinstance(self.x,Constant) or isinstance(self.y,Symbol):
            return f"{self.x}{self.y}"
        if isinstance(self.y,Constant) or isinstance(self.x,Symbol):
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
        return self
    
    def degree(self,var):
        return Constant(self.x.degree(var)) + Constant(self.y.degree(var))
    
    def express(self,x,var):
        return Multiply(self.x.express(x,var),self.y.express(x,var))
    
    def has_variable(self,var):
        return self.x.has_variable(var) or self.y.has_variable(var)

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
            return Multiply(self.x.diff(variable),Multiply(self.y, Power(self.x,self.y-1)))

    
    def __str__(self):
        if isinstance(self.x,Function) and isinstance(self.y,Function):   
            return f"({self.x}) ^ ({self.y})"    
        if isinstance(self.x,Function):
            return f"({self.x}) ^ {self.y}"
        if isinstance(self.y,Function):
            return f"{self.x} ^ ({self.y})"
        return f"{self.x} ^ {self.y}"
    
    def degree(self,var):
        if isinstance(self.y, Constant):
            return self.x.degree(var) * self.y.value
        return 0 
        
    def express(self,x,var):
        return Power(self.x.express(x,var),self.y.express(x,var))
    
    def has_variable(self,var):
        return self.x.has_variable(var) or self.y.has_variable(var)
    
class Trigonometry(Function):

    evaluate=False

    @classmethod
    def evaluatefunc(cls,input):
        cls.evaluate=input

    def __new__(cls,angle):
        if isinstance(angle, (int, float)): angle = Constant(angle)
        obj = super().__new__(cls)
        obj.angle=angle
        return obj.simplified()

    def __init__(self,angle):
        pass
    
    def has_variable(self,var):
        return self.angle.has_variable(var)
    
    def degree(self,var):
        if self.angle.has_variable(var):
            return None
        return 0
    
    def express(self,x,var):
        return type(self)((self.angle.express(x,var)))

class Sin(Trigonometry):
    def simplified(self):
        if isinstance(self.angle,Pi) or self.angle==0:
                return Constant(0)
        if isinstance(self.angle,Multiply):
            if self.angle.x==-1:
                return Multiply(-1,Sin(self.angle.y))
            elif self.angle.y==-1:
                return Multiply(-1,Sin(self.angle.x))
            if any(isinstance(value,Pi) for value in (self.angle.x,self.angle.y)):
                if isinstance(self.angle.x,Pi) and isinstance(self.angle.y,Constant):
                    self.angle.x,self.angle.y=self.angle.y,self.angle.x                 
                self.angle.x=self.angle.x%2
                self.angle.x=round(self.angle.x,10)

                if self.angle.x in (0,1):
                    return Constant(0)
                if self.angle.x==0.5:
                    return Constant(1)
                if self.angle.x==1.5:
                    return Constant(-1)
                
        if Sin.evaluate==True:
            if isinstance(self.angle,Constant):
                return math.sin(self.angle.value)
            if isinstance(self.angle,Multiply):
                if isinstance(self.angle.x,Pi) and isinstance(self.angle.y,Constant):
                    return math.sin(math.pi*self.angle.y)
                if isinstance(self.angle.y,Pi) and isinstance(self.angle.x,Constant):
                    return math.sin(math.pi*self.angle.x)
        return self
    
    def __str__(self):
        return f"sin({self.angle})"
    
    def diff(self,variable):
        return Multiply(Cos(self.angle), self.angle.diff(variable))
    
class Cos(Trigonometry):
    def simplified(self):
        if isinstance(self.angle,Pi):
            return Constant(-1)
        if self.angle==0:
            return Constant(1)
        if isinstance(self.angle,Multiply):
            if self.angle.x==-1:
                return Cos(self.angle.y)
            elif self.angle.y==-1:
                return Cos(self.angle.x)
            if any(isinstance(value,Pi) for value in (self.angle.x,self.angle.y)):
                if isinstance(self.angle.x,Pi) and isinstance(self.angle.y,Constant):
                    self.angle.x,self.angle.y=self.angle.y,self.angle.x                 
                self.angle.x=self.angle.x%2
                self.angle.x=round(self.angle.x,10)

                if self.angle.x in(0.5,1.5):
                    return Constant(0)
                if self.angle.x==0:
                    return Constant(1)
                if self.angle.x==1:
                    return Constant(-1)
                
        if Cos.evaluate==True:
            if isinstance(self.angle,Constant):
                return math.cos(self.angle.value)
            if isinstance(self.angle,Multiply):
                if isinstance(self.angle.y,Pi) and isinstance(self.angle.x,valuetypes):
                    return math.cos(math.pi*self.angle.x)
        return self
    
    def __str__(self):
        return f"cos({self.angle})"
    
    def diff(self,variable):
        return Multiply(self.angle.diff(variable),Multiply(Sin(self.angle), -1))

class Tan(Trigonometry):
    def simplified(self):
        if self.angle==0 or isinstance(self.angle,Pi):
            return Constant(0)
        if isinstance(self.angle,Multiply):
            if self.angle.x==-1:
                return Multiply(-1,Tan(self.angle.y))
            elif self.angle.y==-1:
                return Multiply(-1,Tan(self.angle.x))
            if any(isinstance(value,Pi) for value in (self.angle.x,self.angle.y)):
                if isinstance(self.angle.x,Pi) and isinstance(self.angle.y,Constant):
                    self.angle.x,self.angle.y=self.angle.y,self.angle.x                 
                self.angle.x=self.angle.x%1
                self.angle.x=round(self.angle.x,10)

                if self.angle.x==0:
                    return Constant(0)
                if self.angle.x==0.5:
                    return ZeroDivisionError("Tan(0.5π) is undefined")
                if self.angle.x==0.25:
                    return Constant(1)
                
        if Tan.evaluate==True:
            original = [Sin.evaluate,Cos.evaluate]
            Sin.evaluate,Cos.evaluate=True,True
            output=Divide(Sin(self.angle),Cos(self.angle))
            Sin.evaluate,Cos.evaluate=original
            return output
        return self

    def __str__(self):
        return f"tan({self.angle})"
    
    def diff(self,variable):
        return Multiply(self.angle.diff(variable),Divide(1,Power(Cos(self.angle),2)))

class Ln(Function):
    def __new__(cls,arg):
        if isinstance(arg, (int, float)): arg = Constant(arg)
        obj = super().__new__(cls)
        obj.arg=arg
        return obj.simplified()

    def __init__(self,arg):
        pass

    def simplified(self):
        if self.arg==1:
            return Constant(0)
        if isinstance(self.arg,Euler):
            return Constant(1)
        if isinstance(self.arg,Multiply):
            return Add(Ln(self.arg.x),Ln(self.arg.y))
        if isinstance(self.arg,Power):
            return Multiply(self.arg.y,Ln(self.arg.x))
        return self
    
    def __str__(self):
        return f"ln({self.arg})"

print(Ln(Divide(x,y)))