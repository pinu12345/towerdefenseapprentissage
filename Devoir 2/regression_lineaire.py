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
          cibles =  numpy.array(train_data[:,-1])[:, numpy.newaxis]
          train_data_transform = numpy.concatenate((utilitaires.applyTranform(traits,type=type_transformation),cibles), axis=1)
          numpy.random.seed(3395)
          self.weights = numpy.random.random(train_data_transform.shape[1])
          print 'Shape : ',train_data_transform.shape[1]
          self.weights[-1] = 0
          print 'Weights : ',self.weights
          datas = numpy.array(train_data_transform)
          datas[:,-1] = 1
          n_iter = 0
          n_iter_max = nb_example*1000
          print n_iter_max
          done = False
          gradSum = numpy.zeros((self.weights.shape[0]))
          print 'gradSum'
          print gradSum
          seuil = numpy.exp(-20) 
          print 'seuil'
          print seuil
          i = 0
          capacite = 3
          lamqweer = 0.2
          lamfag = 0.201
          while (not done and (n_iter < n_iter_max)):
                  # calcul du gradient pour l'exemple en cours
                  grad = -datas[i] * (train_data_transform[i,-1] - numpy.dot(datas[i], self.weights))

                  # accumulation des gradients sur l'ensemble d'entrainement
                  gradSum += grad

                  #mise a jour des parametres
                  self.weights -= 2 * self.mu * grad
                  
                  # nous sommes passe au travers de l'ensemble d'entrainement
                  # alors on verifie si la norme de mu * la somme des gradient est plus petite qu'un certain seuil (proche de zero)
                  if (i + 1) == nb_example:
                      if linalg.norm(self.mu*gradSum/nb_example) < seuil:
                          print 'SEUIL ATTEINT'
                          done = True
                      else:
                          gradSum = numpy.zeros((self.weights.shape[0]))
                  i = (i + 1) % nb_example
                  n_iter += 1
          print n_iter
  
	def compute_predictions(self, test_data,type_transformation):
	      # application de la transformation des données
          test_data_transform = utilitaires.applyTranform(test_data, type=type_transformation)
          print 'Test_data_transform'
          print self.weights
          #print test_data_transform
          #return [[5, 5, 1]]
          sorties = []
          for i in range(len(test_data_transform)):
            data = []
            for j in range(len(test_data_transform[i])):
              data.append(test_data_transform[i][j])
            data.append(1)
            sorties.append(numpy.dot(data, self.weights))
          print 'Predictions : '
          #print sorties
          return sorties