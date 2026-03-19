
import math

def babylonianapprox(N,tolerance=10e-10,maxiteration=1000):
    if N<0:
        return ValueError("No negative square roots in babylonianapprox()")
    elif N==0:
        return 0

    a=N
    for _ in range(maxiteration):
        a_n=0.5*(a+(N/a))
        if abs(a_n-a)<tolerance:
            return a_n
        a=a_n


