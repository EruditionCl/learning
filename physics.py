
from utils import *

class Vector3D:
    def __init__(self,x,y,z):
        if x ==0 and y==0 and  z==0:
            raise ValueError("No null vectors allowed")
        self.x=x
        self.y=y
        self.z=z

    def __str__(self):
        return f"{self.x}î + {self.y}ĵ + {self.z}k̂"
    
    def __add__(self,other):
        return Vector3D(self.x+other.x,self.y+other.y,self.z+other.z)
    
    def __eq__(self, other):
        return self.x==other.x and self.y==other.y and self.z==other.z
    
    def __mul__(self,other):
        if isinstance(other,(int,float)):
            return Vector3D(self.x*other,self.y*other,self.z*other)
        else: 
            raise TypeError("In rmul, other variable should be a constant")

    def __rmul__(self,other):
        if isinstance(other,(int,float)):
            return Vector3D(self.x*other,self.y*other,self.z*other)
        else: 
            raise TypeError("In rmul, other variable should be a constant")

    def __matmul__(self, other):
        if isinstance(other, Vector3D):
            return self.x*other.x + self.y*other.y + self.z*other.z
        else:
            raise TypeError("Dot product requires Vector3D")
        
    def __pow__(self,other):
        if isinstance(other, Vector3D):
            return Vector3D(self.x^other.x,self.y^other.y,self.z^other.z)
        else:
            return self.magnitude**other


def inputCOM(dimensions):

    match dimensions:
        case 1:
            objects=[]
            COM=0
            totalmass=0

            numberofobjects=getint("Input how many objects: ")

            for i in range(numberofobjects):
                mass=getfloat("Input mass of object: ")
                coordinate=getfloat("Input coordinate of object: ")
                objects.append([mass,coordinate])
                totalmass+=mass

            for object in objects:
                COM+=object[0]*object[1]

            return (COM/totalmass)


        case 2:
            objects=[]
            COM_x=0
            COM_y=0
            totalmass=0

            numberofobjects=getint("Input how many objects: ")

            for i in range(numberofobjects):
                mass=getfloat("Input mass of object: ")
                x=getfloat("Input x coordinate of object: ")
                y=getfloat("Input y coordinate of object: ")
                objects.append([mass,x,y])
                totalmass+=mass

            for object in objects:
                COM_x+=object[0]*object[1]
                COM_y+=object[0]*object[2]
                
            return [(COM_x/totalmass),(COM_y/totalmass)]
        
        case 3:
            objects=[]
            COM_x=0
            COM_y=0
            COM_z=0
            totalmass=0

            numberofobjects=getint("Input how many objects: ")

            for i in range(numberofobjects):
                mass=getfloat("Input mass of object: ")
                x=getfloat("Input x coordinate of object: ")
                y=getfloat("Input y coordinate of object: ")
                z=getfloat("Input z coordinate of object: ")
                objects.append([mass,x,y,z])
                totalmass+=mass

            for object in objects:
                COM_x+=object[0]*object[1]
                COM_y+=object[0]*object[2]
                COM_z+=object[0]*object[3]
                
            return [(COM_x/totalmass),(COM_y/totalmass),(COM_z/totalmass)]
        
        case _:
            raise ValueError("COM can only be in 1, 2, or 3 dimensions.")
        
        
def sigfigs(value):

    if isinstance(value,str)==False:
        raise TypeError("Value must be a string")

    sigfigs=0
    value = str(value)
    value=value.lstrip("0")
    digits=[digit for digit in value]

    if not "." in digits:
        value=value.rstrip("0") # For string inputs
        digits=[digit for digit in value]
        for _ in digits:
            sigfigs+=1

    elif "." in digits:
        if float(value)<1 and float(value)>0:
            digits.remove(".")
            while digits[0]=="0":
                digits.remove("0")
            for _ in digits:
                sigfigs+=1

        elif float(value)>1:
            digits.remove(".")
            for _ in digits:
                sigfigs+=1

    return sigfigs


def velocity(displacement, time):
    h = 1e-8
    return (displacement(time+h) - displacement(time-h))/(2*h)


def acceleration(velocity, time):
    h = 1e-8
    return (velocity(time+h) - velocity(time-h))/(2*h)



def scientificnotation(input,precision,unit):
    if not isinstance(input,(float,int)) or isinstance(input,bool):
        raise TypeError("input must be a float or int")
    elif not isinstance(precision, (float,int) or isinstance(precision,bool)):
        raise TypeError("precision must be a float or int")

    prefixes = [
        "quetta",
        "ronna",
        "yotta",
        "zetta",
        "exa",
        "peta",
        "tera",
        "giga",
        "mega",
        "kilo",
        "hecto",
        "deca",
        "",
        "deci",
        "centi",
        "milli",
        "micro",
        "nano",
        "pico",
        "femto",
        "atto",
        "zepto",
        "yocto",
        "ronto",
        "quecto",
    ]

    prefixletters=[
        "Q",
        "R",
        "Y",
        "Z",
        "E",
        "P",
        "T",
        "G",
        "M",
        "k",
        "h",
        "da",
        "",
        "d",
        "c",
        "m",
        "μ",
        "n",
        "p",
        "f",
        "a",
        "z",
        "y",
        "r",
        "q",
        
    ]

    input=f"{input:.{precision}e}"

    power=int(input.split("e")[1])
    magnitude=float(input.split("e")[0])

    index=12 

    def result(prefix, k):
        if not k==0:
            print(f"{magnitude*10**(power-k)} {prefixletters[prefix]}{unit[0]} or {magnitude*10**(power-k)} {prefixes[prefix]}{unit}")
        else:
           print(f"{magnitude} {prefixletters[prefix]}{unit[0]} or {magnitude} {prefixes[prefix]}{unit}")


    if power==0:
        result(12,0)
    elif power==1:
        result(11,0)
    elif power==2:
        result(10,0)
    elif power>=3 and power<6:
        result(9,3)
    elif power>=6 and power<9:
        result(8,6)
    elif power>=9 and power<12:
        result(7,9)
    elif power>=12 and power<15:
        result(6,12)
    elif power>=15 and power<18:
        result(5,15)
    elif power>=18 and power<21:
        result(4,18)
    elif power>=21 and power<24:
        result(3,21)
    elif power>=24 and power<27:
        result(2,24)
    elif power>=27 and power<30:
        result(1,27)
    elif power>=30:
        result(0,30)

    elif power==-1:
        result(13,0)
    elif power==-2:
        result(14,0)
    elif power<=-3 and power>-6:
        result(15,-3)
    elif power<=-6 and power>-9:
        result(16,-6)
    elif power<=-9 and power>-12:
        result(17,-9)
    elif power<=-12 and power>-15:
        result(18,-12)
    elif power<=-15 and power>-18:
        result(19,-15)
    elif power<=-18 and power>-21:
        result(20,-18)
    elif power<=-21 and power>-24:
        result(21,-21)
    elif power<=-24 and power>-27:
        result(22,-24)
    elif power<=-27 and power>-30:
        result(23,-27)
    elif power<=-30:
        result(24,-30)