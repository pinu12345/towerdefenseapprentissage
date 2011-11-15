# coding=utf-8
import numpy
#import utilitaires as utilitaires
import utilitaires_corrige as utilitaires
from scipy import linalg

class classif_lineaire:
	def __init__(self, mu):
		self.mu = mu
    
	def train(self, train_data,type_transformation):
          nb_example = train_data.shape[0]
          # application de la transformation des données sur les caratéristiques seules.
          traits = numpy.array(train_data[:,:-1])
          print 'Traits'
          print traits
          cibles =  numpy.array(train_data[:,-1])[:, numpy.newaxis]
          print 'Cibles'
          print cibles
          train_data_transform = numpy.concatenate((utilitaires.applyTranform(traits,type=type_transformation),cibles), axis=1)
          self.weights = numpy.random.random(train_data_transform.shape[1])
          print 'Shape : ',train_data_transform.shape[1]
          self.weights[-1] = 0
          print 'Weights : ',self.weights
          datas = numpy.array(train_data_transform)
          datas[:,-1] = 1
          print 'Train Data : '
          print datas
          n_iter = 0
          n_iter_max = nb_example*1000
          print n_iter_max
          done = False
          gradSum = numpy.zeros((self.weights.shape[0]))
          print 'gradSum'
          print gradSum
          seuil = numpy.exp(-20) 
          #seuil = 0.0000000000001
          print 'seuil'
          print seuil
          i = 0
          while (not done and (n_iter < n_iter_max)):
                  # calcul du gradient pour l'exemple en cours
                  grad = -datas[i] * (train_data_transform[i,-1] - numpy.dot(datas[i], self.weights))
                  # accumulation des gradients sur l'ensemble d'entrainement
                  gradSum += grad
                  #print i, n_iter, nb_example
                  # mise a jour des parametres
                  
                  ## Self.weights doit etre self.mu * somme des grads? + lambda[Hyperparametre] sigma(teta)
                  ##-> Mettre lorsque l'on a parcouru tous les points? self.weights -= ...
                  self.weights -= 2 * self.mu * grad
                  # nous sommes passe au travers de l'ensemble d'entrainement
                  # alors on verifie si la norme de mu * la somme des gradient est plus petite qu'un certain seuil (proche de zero)
                  if (i + 1) == nb_example:
                      if linalg.norm(self.mu*gradSum/nb_example) < seuil:
                          # Fin de l'entrainement.
                          print 'SEUIL ATTEINT'
                          done = True
                      else:
                          #self.weights -= 2 * self.mu * gradSum
                          print 'Current gradSum:'
                          print linalg.norm(self.mu*gradSum/nb_example)
                          print seuil
                          print gradSum
                          gradSum = numpy.zeros((self.weights.shape[0]))
                          #print gradSum
                          print 'Weights :'
                          print self.weights
                  i = (i + 1) % nb_example
                  n_iter += 1
          print n_iter
  
	def compute_predictions(self, test_data,type_transformation):
	        # application de la transformation des données
          test_data_transform = utilitaires.applyTranform(test_data, type=type_transformation)
          sorties = []
          for i in range(len(test_data_transform)):
            data = []
            for j in range(len(test_data_transform[i])):
              data.append(test_data_transform[i][j])
            data.append(1)
            sorties.append(numpy.dot(data, self.weights))
          return sorties
