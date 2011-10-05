# coding=utf-8
import numpy
import utilitaires

class parzen:

    def __init__(self,n_classes):
        self.n_classes = n_classes

    def train(self, train_data):
        self.train_data = train_data

    # Question 1
    def K(self, x, Y, variance = 0.5):
        return numpy.exp(-numpy.sum((x-Y)**2.0/(2.0*(variance**2.0)),axis=1))

    # Questions 2 et 3
    def compute_predictions(self, test_data):

        num_test = test_data.shape[0]
        les_poids = numpy.zeros((num_test,self.n_classes))

        for (i,ex) in enumerate(test_data):

            num = numpy.zeros(self.n_classes) ## Somme pondérée des observations
            den = 0 ## Pondération totale
            valeur = numpy.zeros(self.n_classes)

            poids = self.K(ex,self.train_data[:,:-1])

            for j in range(len(poids)):
                num[self.train_data[j,-1]-1] += poids[j]
                den += poids[j]
                valeur = num/den
            les_poids[i,:] = valeur

        return les_poids