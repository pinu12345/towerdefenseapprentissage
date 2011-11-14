from numpy import *
from Dn import *
import pylab

def regression_gradient(w, b, lam, pas):
    print "regression"

def regression_analytique(w, b, X, lam):
    pass

def numero4():
    Dn = generateDn(15)
    #Dn2 = generateDn(20)
    #Dn3 = generateDn(10)
    pylab.plot(Dn[0],Dn[1], 'ro')
    #h2 = pylab.plot(Dn2)
    #h3 = pylab.plot(Dn3)
    #labels = ['h1','h2','h3']    
    #handles = [h1, h2, h3]
    #pylab.legend(handles,labels)
    pylab.grid(True)
    pylab.axis([-5,5,-10,10])
    pylab.show()

def main():
    numero4()
    
if __name__ == "__main__":
    main()