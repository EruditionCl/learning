

def getfloat(x):
    while True:
        try:
            return float(input(x))
        except ValueError:
            print("Invalid")

def getint(x):
    while True:
        try:
            return int(input(x))
        except ValueError:
            print("Invalid")

def getpositive(x):
    while True:
        try:
            y = float(input(x))
            if y<0:
                print("Invalid")
                continue
            return y
        except ValueError:
            print("Invalid")







