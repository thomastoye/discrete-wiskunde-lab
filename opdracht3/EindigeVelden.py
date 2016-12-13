
import fractions
import sys
import numpy as np
from sympy import *
x= symbols('x')
z = "2"

g= x**8+x**4+x**3+x+1
f =x**6+x**4+x**3+x+1


#g = x**7+x**5+x**4+x**3+x+1
#f = x**4+x+1

def findBezout(f,g):
    print("GGD("+str(f)+","+str(g)+")")

    test = []
    while (f != 0):
        #euclidische deling uitvoeren
        q, r = div(g, f,x)

        #rest en quotient conververten naar polynoom
        polyrest = r.as_poly(x,domain='GF('+z+')')
        polyquotient = q.as_poly(x,domain='GF('+z+')')

        #waarden uit polynoom halen
        rest = polyrest.args[0]
        quotient = polyquotient.args[0]

        print("=ggd({0}, {1} mod {0})".format(f,g))
        print("\t{1} = {0} * {2} + {3}".format(f,g,quotient,rest))

        test.append([g, f, rest, quotient])
        g = f
        f = rest

    r1 = test[0][3]
    q1 = test[0][2]
    q2 = test[1][2]
    if (r1 == 1):
        alpha = -q1
        beta = 1
    else:
        alpha = (1 + q1*q2).expand()
        beta = -q2

    alpha = alpha.as_poly(x, domain='GF(' + z + ')').args[0]
    beta = beta.as_poly(x, domain='GF(' + z + ')').args[0]

    print("alpha={0}, beta={1}, gcd={2}".format(alpha, beta, g))
    inverse = beta

    testIfOne = (f*inverse).expand()
    testIfOne = testIfOne.as_poly(x, domain='GF(' + z + ')').args[0]
    print("This should be one:", testIfOne)

    return inverse

#print("ResttTestje", polyrest, "Quotient", polyquotient  )




#gcd(f, g, x)

#print(gcd(f, g, x))

#euclidische deling uitvoeren

inv = findBezout(f,g)
print("inverse:", inv)



#print(pdiv(result[0],2))
#print(pdiv(x**6+x**4+x**3+x+1, x**5+x**3+x**2))
