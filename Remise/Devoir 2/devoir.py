from scipy import linalg
import pylab, numpy, math, random

numpy.random.seed(100)

def main():
    #Pour le numero 4 on produit uniquement un graphique avec lam = 0, k = 1
    if 1:
        print 'Numero 4 :'
        numero4()
        print 'Fin du Numero 4'
        print ''
    
    #Pour le numero 5 on produit des graphiques pour lam = 0.0001, 0.0007 avec k = 1
    if 1:
        print 'Numero 5 :'
        for vallam in [0.001, 0.007]:
            print 'Lambda = ' + str(vallam)
            numero5(lam = vallam)
        print 'Fin du Numero 5'
        print ''

    #Pour le numero 6 on produit des graphiques avec lam = 0 pour k = 1, 2, 3
    if 1:
        print 'Numero 6 :'
        for valk in [1, 2, 3]:
            print 'K = ' + str(valk)
            numero6(lam = 0, k = valk)
        print 'Fin du Numero 6'
        print ''

    #Pour le numero 7 on produit des graphiques avec lam = 0, 5, 20 pour k = 1, 2, 3, 10
    if 1:
        print 'Numero 7 :'
        for valk in [1, 2, 3, 10]:
            for vallam in [0, 5, 20]:
                print 'K = ' + str(valk) + ', Lambda = ' + str(vallam)
                numero7(lam = vallam, k = valk)
        print 'Fin du Numero 7'
        print ''

    #Pour le numero 8 on produit des graphiques sur ellipse.txt avec lam = 0, 5, 20 pour k = 1, 2, 3, 4
    if 1:
        print 'Numero 8 :'
        for valk in [1, 2, 3, 4]:
            for vallam in [0, 5, 20]:
                print 'K = ' + str(valk) + ', Lambda = ' + str(vallam)
                numero8(lam = vallam, k = valk)
        print 'Fin du Numero 8'
        print ''

def h(x):
    return numpy.sin(x) + 0.3 * x - 1
    
##Generation de Dn pour le numero 3 (Dn = generateDn(15))
def generateDn(n):
    random.seed(100)
    Dn = numpy.zeros([n,2])
    for i in range(n):
        x = random.uniform(-5,5)
        Dn[i,0] = x
        Dn[i,1] = h(x)
    return Dn

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
            addedTrait = numpy.array(data**i)
            if transformData == []:
                transformData = addedTrait
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
    print 'Regression Gradient [w*, b*]: ', weights
    return weights
    
def regression_analytique(Dn, lam = 1, type_transformation = -1, k = 0):
    X = numpy.concatenate((numpy.ones([len(Dn),1]), applyTranform(Dn[:,:-1],type=type_transformation,k=k)), axis = 1)
    Xt = X.transpose()
    t = Dn[:,-1]
    I = numpy.eye(X.shape[1])
    I[0][0] = 0
    result = numpy.dot(linalg.inv(numpy.dot(Xt, X) + lam * I), numpy.dot(Xt, t))
    print 'Regression Analytique [b*, w*]: ', result
    return result 

def numero4(lam = 0, k = 1, type_transformation = -1):
    # On genere Dn
    Dn = generateDn(15)
    
    # On genere les points pour la fonction h(x)
    x = numpy.arange(-10, 10, 0.1)

    # On genere le w et b par regression analytique
    analytique = regression_analytique(Dn, lam, type_transformation, k)
    analPlot = analytique[0]
    for i in range(1, len(analytique)):
        analPlot += x ** i * analytique[i]
    
    # On genere le w et b par regression lineaire regularisee
    reglinreg = regression_gradient(Dn, lam, type_transformation, k)
    gradPlot = reglinreg[-1]
    for i in range(0, len(reglinreg)-1):
        gradPlot += x ** (i+1) * reglinreg[i]
    
    pylab.plot(Dn[:,0],Dn[:,1], 'ro', x, h(x), 'k', x, analPlot, 'b', x, gradPlot, 'r')

    #Show the graph
    labels = ['Dn','h(x)', 'Analytique', 'Regression Lineaire']
    pylab.title('Lambda = ' + str(lam))
    pylab.legend(labels)
    pylab.grid(True)
    pylab.axis([-10,10,-10,10])
    pylab.show()
    
def numero5(lam = 0):
    numero4(lam)

def numero6(lam = 0, k = 1, type_transformation = 4):
    # On genere Dn
    Dn = generateDn(8)
    
    # On genere les points pour la fonction h(x)
    x = numpy.arange(-10, 10, 0.1)

    # On genere le w et b par regression analytique
    analytique = regression_analytique(Dn, lam, type_transformation, k)
    analPlot = analytique[0]
    for i in range(1, len(analytique)):
        analPlot += x ** i * analytique[i]
    
    # On genere le w et b par regression lineaire regularisee
    reglinreg = regression_gradient(Dn, lam, type_transformation, k)
    gradPlot = reglinreg[-1]
    for i in range(0, len(reglinreg)-1):
        gradPlot += x ** (i+1) * reglinreg[i]

    #Show the graph
    pylab.plot(Dn[:,0],Dn[:,1], 'ro', x, h(x), 'k', x, analPlot, 'b', x, gradPlot, 'r')
    labels = ['Dn','h(x)', 'Analytique', 'Regression Lineaire']
    pylab.title('K = ' + str(k) + ', Lambda = ' + str(lam))
    pylab.legend(labels)
    pylab.grid(True)
    pylab.axis([-10,10,-10,10])
    pylab.show()

def numero7(lam = 0, k = 1, type_transformation = 4):
    # On genere Dn
    Dn = generateDn(15)
    
    # On genere les points pour la fonction h(x)
    x = numpy.arange(-10, 10, 0.1)

    # On genere le w et b par regression analytique
    analytique = regression_analytique(Dn, lam, type_transformation, k)
    analPlot = analytique[0]
    for i in range(1, len(analytique)):
        analPlot += x ** i * analytique[i]
    pylab.plot(Dn[:,0],Dn[:,1], 'ro', x, h(x), 'k', x, analPlot, 'b')

    labels = ['Dn','h(x)', 'Analytique']
    pylab.title('K = ' + str(k) + ', Lambda = ' + str(lam))
    pylab.legend(labels)
    pylab.grid(True)
    pylab.axis([-10,10,-10,10])
    pylab.show()

def numero8(lam = 0, k = 1, type_transformation = 4):
    # On load ellipse.txt
    x = numpy.arange(-10, 10, 0.1)
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

    analytique = regression_analytique(train_set, lam, type_transformation, k)
    analPlot = analytique[0]
    for i in range(1, len(analytique)):
        analPlot += x ** i * analytique[i]
    pylab.plot(train_set[:,0], train_set[:,1], 'ro', x, analPlot, 'b')
    labels = ['4 Points d\'ellipse.txt', 'Analytique']
    pylab.title('K = ' + str(k) + ', Lambda = ' + str(lam))
    pylab.legend(labels)
    pylab.grid(True)
    pylab.axis([-10,10,-20,20])
    pylab.show()

if __name__ == "__main__":
    main()