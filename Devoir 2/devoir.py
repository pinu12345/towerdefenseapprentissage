from GenerateDn import *
from scipy import linalg
import pylab, numpy

numpy.random.seed(100)

def h(x):
    return numpy.sin(x) + 0.3 * x - 1

def applyTranform(data, sigma=0, type=2, k=1):
        transformData = []
        # transformation = (xi, .... xd, sigma*xi*...*xd)
        if type == 1:
          addedTrait = numpy.array(numpy.prod(data, axis=1)) * sigma
          addedTrait = addedTrait[:,numpy.newaxis]
          transformData = numpy.concatenate((data,addedTrait), axis=1)
        # transformation = (x1^2, x2^2, sigma*x1*x2)
        elif type == 2:
          addedTrait = numpy.array(numpy.prod(data, axis=1)) * sigma
          addedTrait = addedTrait[:,numpy.newaxis]
          transformData = numpy.concatenate((data**2,addedTrait), axis=1)
        # transformation = (x1,x2,x1^2+x2^2)
        elif type == 3:
          addedTrait = numpy.array(numpy.sum(data**2, axis=1)) * sigma
          addedTrait = addedTrait[:,numpy.newaxis]
          transformData = numpy.concatenate((data,addedTrait), axis=1)
        # transformation 
        elif type == 4:
          for i in range(1,k+1):
            #print 'Data:', k
            #print data
            #print data**i
            addedTrait = numpy.array(data**i)
            if transformData == []:
                #print 'addedTrait'
                #print addedTrait
                transformData = addedTrait
                #print transformData
            else:
                transformData = numpy.concatenate((transformData, addedTrait), axis=1)
        # no transformation
        else:
          transformData = numpy.array(data)
        return transformData

def regression_gradient(Dn, lam = 0.0001, type_transformation = -1, k = 0, mu = 0.0005):
    X = Dn[:,:-1]
    t = Dn[:,-1:]
    nb_example = len(X)
    train_data_transform = numpy.concatenate((applyTranform(X,type=type_transformation,k=k),t), axis=1)
    weights = numpy.random.random(train_data_transform.shape[1])
    weights[-1] = 0
    datas = numpy.array(train_data_transform)
    datas[:,-1] = 1
    n_iter = 0
    n_iter_max = nb_example*1000
    done = False
    gradSum = numpy.zeros((weights.shape[0]))
    seuil = numpy.exp(-20) 
    i = 0
    while (not done and (n_iter < n_iter_max)):
        grad = -datas[i] * (train_data_transform[i,-1] - numpy.dot(datas[i], weights))
        gradSum += grad
        weights -= (2 * mu * grad - lam * linalg.norm(weights)**2)
        if (i + 1) == nb_example:
            if linalg.norm(mu*gradSum/nb_example) < seuil:
                done = True
            else:
                gradSum = numpy.zeros((weights.shape[0]))
        i = (i + 1) % nb_example
        n_iter += 1
    print 'Regression Gradient : ', weights
    return weights
    
def regression_analytique(Dn, lam = 1, type_transformation = -1, k = 0):
    X = numpy.concatenate((numpy.ones([len(Dn),1]), applyTranform(Dn[:,:-1],type=type_transformation,k=k)), axis = 1)
    Xt = X.transpose()
    t = Dn[:,-1]
    I = numpy.eye(X.shape[1])
    I[0][0] = 0
    result = numpy.dot(linalg.inv(numpy.dot(Xt, X) + lam * I), numpy.dot(Xt, t))
    print 'Regression Analytique : ', result
    return result 

def numero4():
    # Parametres
    lam = 0
    type_transformation = 4
    k = 4

    # On genere Dn
    Dn = generateDn(4)
    
    # On genere les points pour la fonction h(x)
    x = numpy.arange(-10, 10, 0.1)

    # On genere le w et b par regression analytique
    analytique = regression_analytique(Dn, lam, type_transformation, k)
    analPlot = analytique[0]
    for i in range(1, len(analytique)):
        analPlot += x ** i * analytique[i]
    pylab.plot(Dn[:,0],Dn[:,1], 'ro', x, h(x), 'k', x, analPlot, 'b')
    
    # On genere le w et b par regression lineaire regularisee
    #reglinreg = regression_gradient(Dn, lam, type_transformation, k)
    #gradPlot = reglinreg[-1]
    #for i in range(0, len(reglinreg)-1):
        #gradPlot += x ** (i+1) * reglinreg[i]
    #pylab.plot(Dn[:,0],Dn[:,1], 'ro', x, h(x), 'k', x, gradPlot, 'b')

    #Show the graph
    #labels = ['Dn','h(x)', 'Analytique (lambda = 0.001)', 'Regression Lineaire (lambda = 0.001)']
    #labels = ['Dn','h(x)', 'Analytique (k = ' + str(k) + ')', 'Regression Lineaire (k = ' + str(k) + ')']
    labels = ['Dn','h(x)', 'Analytique (k = ' + str(k) + ')']
    #labels = ['Dn','h(x)', 'Regression Lineaire (k = ' + str(k) + ')']
    pylab.legend(labels)
    pylab.grid(True)
    pylab.axis([-10,10,-10,10])
    pylab.show()

def numero8():
    # Parametres
    lam = 20
    type_transformation = 4
    k = 4
    x = numpy.arange(-10, 10, 0.1)
    
    # On load ellipse.txt
    data = numpy.loadtxt('ellipse.txt')
    train_cols = [0]
    target_ind = [data.shape[1] - 2]
    n_classes = 2
    n_train = 4 #Peu de points d'apprentissage pour voir l'effet de la regularisation
    
    random.seed(3395)
    
    inds = range(data.shape[0])
    random.shuffle(inds)
    train_inds = inds[:n_train]
    train_set = data[train_inds,:]
    train_set = train_set[:,train_cols + target_ind]

    print 'Train_set :'
    print train_set
    
    analytique = regression_analytique(train_set, lam, type_transformation, k)
    analPlot = analytique[0]
    for i in range(1, len(analytique)):
        analPlot += x ** i * analytique[i]
    pylab.plot(train_set[:,0], train_set[:,1], 'ro', x, analPlot, 'b')
    labels = ['4 Points d\'ellipse.txt', 'Analytique (k = ' + str(k) + ', lambda = ' + str(lam) + ')']
    pylab.legend(labels)
    pylab.grid(True)
    pylab.axis([-10,10,-20,20])
    pylab.show()
    
def main():
    #numero4()
    numero8()

if __name__ == "__main__":
    main()

#http://mechanistician.blogspot.com/2009/02/lecture-2-linear-regression-part-2.html
#http://pyml.sourceforge.net/tutorial.html