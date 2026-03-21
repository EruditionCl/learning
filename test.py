
import math as math
import time as time


def setconstant(*args): # Takes ints or floats and converts them to Constant()
    result = []
    for arg in args:
        if isinstance(arg, (int, float)):
            result.append(Constant(arg))
        else:
            result.append(arg)
    return tuple(result)

def factorial(input):
    if not isinstance(input,int):
        raise TypeError("input in factorial() must be a int")
    elif input<0:
        raise ValueError("input in factorial() must be greater than zero")
    elif input==0:
        return 1
    else:
        final=1
        for i in range(input):
            final*=(i+1)
        return final

class Expression: # Parent Class
    def __init__(self):
        pass
    
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

    def __rpow__(self,other):
        return Power(other,self)
    
    def __neg__(self):
        return Multiply(-1,self)

    def __pos__(self):
        return self
    
    def orderdiff(self,variable,n=1):
        for _ in range(n):
            self=self.diff(variable)
        return self

    def taylor(self,variable,n=10,a=0):
        final=0
        for i in range(n):
            func=self.orderdiff(variable,i)
            funcexpress=func.express(a,variable)
            polynomial=(variable-a)**i
            final=(funcexpress*polynomial)/factorial(i)+final
        return final

class Identifier(Expression):
    def __init__(self):
        pass

class Value(Identifier): 
    def __init__(self):
        pass

    def diff(self,variable): #Differentiating a constant returns 0
        return 0
    
    def simplified(self):
        return self
    
    def express(self, x, var): #If f(x) = 3, if x=0 then f(x) is still 3
        return self
    
    def degree(self,var): #Degree of a constant is 0
        return 0
    
    def has_variable(self,var):
        return False
    
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

class Constant(Value):
    def __init__(self,value):
        if isinstance(value,Constant):
            value=value.value

        if not any(isinstance(value, type) for type in (float,int)):
            raise ValueError("Constant only accepts float or int")
        self.value=value 
    
    def __str__(self):
        return f"{self.value}"
    
    def __eq__(self, other): #The following magic methods accounts for int & floats being accepted
        if isinstance(other, Constant):
            return self.value == other.value
        if isinstance(other, (int, float)):
            return self.value == other
        return False
    
    def __add__(self,other):
        if isinstance(other,(int,float)):
            return Constant(self.value+other)
        if isinstance(other,Constant):
            return Constant(self.value+other.value)
        return Add(self.value,other)
    
    def __sub__(self,other):
        if isinstance(other,(int,float)):
            return Constant(self.value-other)
        if isinstance(other,Constant):
            return Constant(self.value-other.value)
        return Substract(self.value,other)

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
        if isinstance(other,Constant):
            return Constant(self.value/other.value)
        return Divide(self.value,other)
    
    def __pow__(self,other):
        if isinstance(other,(int,float)):
            return Constant(self.value**other)
        if isinstance(other,Constant):
            return Constant(self.value**other.value)
        return Power(self.value,other)
    
    def __round__(self, ndigits=10):
        return round(self.value,ndigits)

class Symbol(Value):
    def __init__(self):
        pass

    def __eq__(self,other):
        return isinstance(other,type(self))

class Euler(Symbol):
    def __init__(self):
        self.value=2.718281828459045
        super().__init__()
    
    def __str__(self):
        return "e"

class Pi(Symbol):
    def __init__(self):
        self.value=3.1415926358979
        super().__init__()
    
    def __str__(self):
        return "π"



class Variable(Identifier):
    def __init__(self,symbol):
        self.symbol=symbol

    def diff(self,variable):
        if variable==self:
            return 1
        else:
            return 0

    def degree(self,var):
        if self.symbol==var:
            return 1
        return 0

    def express(self, x, var):
        if var==self:
            return Constant(x)
        return self
    
    def has_variable(self,var): #If var==None, then it looks for any variable not a specific variable
        if var==None:
            return True
        return self.symbol==var
        
    def __str__(self):
        return f"{self.symbol}"


x=Variable("x") # Easy to just store it here instead of typing it manually for every test
y=Variable("y")
z=Variable("z")
e=Euler()
pi=Pi()
π=pi
valuetypes = (Constant,int,float)

class Function(Expression): # Functions
    def __init__(self):
        pass

class Unary(Function):

    evaluate=False

    @classmethod
    def evaluatefunc(cls,input):
        cls.evaluate=input

    def __new__(cls,arg):
        arg,=setconstant(arg)
        obj = super().__new__(cls)
        obj.arg=arg
        return obj.simplified()

    def __init__(self,arg):
        pass
    
    def has_variable(self,var):
        return self.arg.has_variable(var)
    
    def degree(self,var):
        if self.arg.has_variable(var):
            return None
        return 0
    
    def express(self,x,var):
        return type(self)((self.arg.express(x,var)))

class Binary(Function):
    def __new__(cls,x,y):
        x,y=setconstant(x,y)
        obj = super().__new__(cls)
        obj.x,obj.y=x,y
        return obj.simplified()

    def __init__(self,x,y):
        pass

    def has_variable(self,var):
        return self.x.has_variable(var) or self.y.has_variable(var)

class Add(Binary):

    def diff(self,variable):
        return Add(self.x.diff(variable),self.y.diff(variable))
    
    def __str__(self):
        left,right=f"{self.x}",f"{self.y}"
        if isinstance(self.x,(Power,Exp,NaturalExp)):
            left=f"({self.x})"
        if isinstance(self.y,(Power,Exp,NaturalExp)):
            right=f"({self.y})"
        return f"{left} + {right}"
    
    def simplified(self):
        if self.x == 0: 
            return self.y
        if self.y == 0: 
            return self.x
        if self.x==self.y: 
            return Multiply(2,self.x)
        if all(isinstance(expr,Constant) for expr in (self.x,self.y)): 
            return Constant(self.x+self.y)
        if isinstance(self.x, Constant) and not isinstance(self.y, Constant):
            return Add(self.y,self.x)
        if isinstance(self.x, Variable) and isinstance(self.y, Multiply):
            if self.x == self.y.y:
                return Multiply(Add(1,self.y.x),self.x)
        if isinstance(self.y, Variable) and isinstance(self.x, Multiply):
            if self.y == self.x.y:
                return Multiply(Add(1,self.x.x),self.y)
        if isinstance(self.x, Multiply) and isinstance(self.y, Multiply):
            if self.x.y == self.y.y:
                return Multiply(Add(self.x.x,self.y.x),self.x.y)
        if isinstance(self.x, Multiply) and isinstance(self.y, Add):
            if isinstance(self.y.x, Multiply): 
                if self.x.y == self.y.x.y: 
                    return Add(Multiply(Add(self.x.x,self.y.x.x),self.x.y),self.y.y)
        if isinstance(self.x,Power) and isinstance(self.x.x,Sin) and self.x.y==2:
            if isinstance(self.y,Power) and isinstance(self.y.x,Cos) and self.y.y==2:
                if self.x.x.arg==self.y.x.arg:
                    return Constant(1)
        if isinstance(self.x, Add):
                return Add(self.x.x,Add(self.x.y,self.y))
        return self
      
    def degree(self,var):
        return max(self.x.degree(var),self.y.degree(var))
    
    def express(self,x,var):
        return self.x.express(x,var)+self.y.express(x,var)

class Multiply(Binary):
    def diff(self,variable):
        return Add(Multiply(self.x.diff(variable),self.y),Multiply(self.y.diff(variable),self.x))
    
    def __str__(self):
        if self.x==-1:
            return f"-{self.y}"
        if self.y==-1:
            return f"-{self.x}"
        if isinstance(self.x,Function) and isinstance(self.y,Function):
            return f"({self.x})({self.y})"
        if isinstance(self.x,Function) and isinstance(self.y,Identifier):
            return f"{self.y}({self.x})"
        if isinstance(self.y,Function) and isinstance(self.x,Identifier):
            return f"{self.x}({self.y})"
        if isinstance(self.x,Constant) or isinstance(self.y,Symbol):
            return f"{self.x}{self.y}"
        if isinstance(self.y,Constant) or isinstance(self.x,Symbol):
            return f"{self.y}{self.x}"
        
    
    def simplified(self):
        if any(value==0 for value in (self.x,self.y)):
            return 0
        if self.x==1:
            return self.y
        elif self.y==1:
            return self.x
        if all(isinstance(expr,Constant) for expr in (self.x,self.y)):
            return Constant(self.x*self.y)
        if self.x==self.y:
            return Power(self.x,2)
        if isinstance(self.x,Power):
            if self.x.x==self.y:
                return Power(self.x.x,Add(self.x.y,1))
        if isinstance(self.y,Power):
            if self.y.x==self.x:
                return Power(self.y.x,Add(self.y.y,1))
        if isinstance(self.x,Power) and isinstance(self.y,Power):
            if self.x.x==self.y.x:
                return Power(self.x.x,Add(self.x.y,self.y.y))
        if isinstance(self.x, Multiply):
                return Multiply(self.x.x,Multiply(self.x.y,self.y))
        return self
    
    def degree(self,var):
        return self.x.degree(var) + self.y.degree(var)
    
    def express(self,x,var):
        return self.x.express(x,var)*self.y.express(x,var)

class Substract(Binary):
    def __new__(cls,x,y):
        x,y=setconstant(x,y)
        return x + -y

class Divide(Binary):
    def __new__(cls,x,y):
        x,y=setconstant(x,y)
        return x * y**-1
    
class Power(Binary):
    def simplified(self):
        if all(isinstance(value,Constant) for value in (self.x,self.y)):
            return Constant(self.x**self.y)
        if self.y==0:
            return 1
        if self.y==1:
            return self.x
        if isinstance(self.x,Power):
            return Power(self.x.x,Multiply(self.x.y,self.y))
        if self.x==e:
            return NaturalExp(self.y)
        if self.y.has_variable(None):
            return Exp(self.x,self.y)
        return self
    
    def diff(self,variable): 
            return Multiply(Multiply(self.y,Power(self.x,Substract(self.y,1))),self.x.diff(variable))

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
        return self.x.express(x,var)**self.y.express(x,var)

class Sin(Unary):
    def simplified(self):
        if self.arg==π or self.arg==0:
                return 0
        if isinstance(self.arg,Multiply):
            if self.arg.x==-1:
                return -Sin(self.arg.y)
            elif self.arg.y==-1:
                return -Sin(self.arg.x)
            if any(value==π for value in (self.arg.x,self.arg.y)):
                if self.arg.x==π and isinstance(self.arg.y,valuetypes):
                    self.arg.x,self.arg.y=self.arg.y,self.arg.x                 
                self.arg.x=self.arg.x%2
                self.arg.x=round(self.arg.x,10)

                if self.arg.x in (0,1):
                    return 0
                if self.arg.x==0.5:
                    return 1
                if self.arg.x==1.5:
                    return -1
                
        if Sin.evaluate==True:
            if isinstance(self.arg,valuetypes):
                return Sin(x).taylor(x,20).express(self.arg.value,x)
            if isinstance(self.arg,Multiply):
                if self.arg.x==π and isinstance(self.arg.y,valuetypes):
                    return Sin(x).taylor(x,20).express(pi.value*self.arg.y,x)
                if self.arg.y==π and isinstance(self.arg.x,valuetypes):
                    return Sin(x).taylor(x,20).express(pi.value*self.arg.x,x)
        return self
    
    def __str__(self):
        return f"sin({self.arg})"
    
    def diff(self,variable):
        return Cos(self.arg)*self.arg.diff(variable)
    
class Cos(Unary):
    def simplified(self):
        if self.arg==π:
            return -1
        if self.arg==0:
            return 1
        if isinstance(self.arg,Multiply):
            if self.arg.x==-1:
                return Cos(self.arg.y)
            elif self.arg.y==-1:
                return Cos(self.arg.x)
            if any(value==π for value in (self.arg.x,self.arg.y)):
                if self.arg.x==pi and isinstance(self.arg.y,valuetypes):
                    self.arg.x,self.arg.y=self.arg.y,self.arg.x                 
                self.arg.x=self.arg.x%2
                self.arg.x=round(self.arg.x,10)

                if self.arg.x in(0.5,1.5):
                    return 0
                if self.arg.x==0:
                    return 1
                if self.arg.x==1:
                    return -1
                
        if Cos.evaluate==True:
            if isinstance(self.arg,Constant):
                return Cos(x).taylor(x,20).express(self.arg.value,x)
            if isinstance(self.arg,Multiply):
                if self.arg.y==π and isinstance(self.arg.x,valuetypes):
                    return Cos(x).taylor(x,20).express(pi.value*self.arg.x,x)
        return self
    
    def __str__(self):
        return f"cos({self.arg})"
    
    def diff(self,variable):
        return self.arg.diff(variable)*-Sin(self.arg)

class Tan(Unary):
    def simplified(self):
        if self.arg==0 or self.arg==π:
            return 0
        if isinstance(self.arg,Multiply):
            if self.arg.x==-1:
                return -Tan(self.arg.y)
            elif self.arg.y==-1:
                return -Tan(self.arg.x)
            if any(value==π for value in (self.arg.x,self.arg.y)):
                if self.arg.x==π and isinstance(self.arg.y,valuetypes):
                    self.arg.x,self.arg.y=self.arg.y,self.arg.x                 
                self.arg.x=self.arg.x%1
                self.arg.x=round(self.arg.x,10)

                if self.arg.x==0:
                    return 0
                if self.arg.x==0.5:
                    return ZeroDivisionError("Tan(0.5π) is undefined")
                if self.arg.x==0.25:
                    return 1
                
        if Tan.evaluate==True:
            original = [Sin.evaluate,Cos.evaluate]
            Sin.evaluate,Cos.evaluate=True,True

            output=Sin(self.arg)/Cos(self.arg)
            Sin.evaluate,Cos.evaluate=original
            return output
        return self

    def __str__(self):
        return f"tan({self.arg})"
    
    def diff(self,variable):
        return self.arg.diff(variable)*Cos(self.arg)**(-2)

class Ln(Unary):
    def simplified(self):
        if self.arg==1:
            return 0
        if self.arg==e:
            return 1
        if isinstance(self.arg,Multiply):
            return Ln(self.arg.x)+Ln(self.arg.y)
        if isinstance(self.arg,Power):
            return self.arg.y*Ln(self.arg.x)
        if isinstance(self.arg, Exp):
            return self.arg.arg
        
        if Ln.evaluate==True:
            if isinstance(self.arg,Constant):
                return math.log(self.arg.value)
        return self
    
    def diff(self,variable):
        return self.arg.diff(variable)/self.arg
    
    def __str__(self):
        return f"ln({self.arg})"    

class NaturalExp(Unary):
    def simplified(self):
        if self.arg==0:
            return 1
        if self.arg==1:
            return e
        if isinstance(self.arg,Ln):
            return self.arg.arg
        return self
    
    def diff(self,variable):
        return self*self.arg.diff(variable)

    def __str__(self):
        if isinstance(self.arg,Function):   
            return f"e ^ ({self.arg})"
        return f"e ^ {self.arg}"

class Exp(Binary):
    def degree(self,var):
        if self.y.has_variable(var):
            return None
        return 0
    
    def express(self,x,var):
        return self.y.express(x,var)

    def simplified(self):
        if self.x==1:
            return 1
        elif self.x==0:
            return 0 
        elif self.x==e:
            return NaturalExp(self.y)
        if isinstance(self.y,valuetypes):
            return Power(self.x,self.y)
        return self

    def diff(self,variable):
        return self*(self.y*Ln(self.x)).diff(variable)
    
    def __str__(self):
        if isinstance(self.x,Function) and isinstance(self.y,Function):   
            return f"({self.x}) ^ ({self.y})"    
        if isinstance(self.x,Function):
            return f"({self.x}) ^ {self.y}"
        if isinstance(self.y,Function):
            return f"{self.x} ^ ({self.y})"
        return f"{self.x} ^ {self.y}"

