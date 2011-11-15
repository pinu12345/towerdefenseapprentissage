# coding=utf-8
import numpy
import utilitaires_corrige as utilitaires
import pdb 

class perceptron:
	def __init__(self, mu):
		self.mu = mu
    
	def train(self, train_data,type_transformation=-1):
          print train_data.shape
          nb_example = train_data.shape[0]
          # application de la transformation des données sur les caratéristiques seules.
          traits = numpy.array(train_data[:,:-1])
          cibles =  numpy.array(train_data[:,-1])[:, numpy.newaxis]
          train_data_transform = numpy.concatenate((utilitaires.applyTranform(traits,type=type_transformation),cibles), axis=1) 

          self.weights = numpy.random.random(train_data_transform.shape[1])
          self.weights[-1] = 0
          datas = numpy.array(train_data_transform)
          datas[:,-1] = 1
          i = 0
          count = 0 # We stop when the set is linearly separated
          n_iter = 0
          n_iter_max = nb_example*100
          while (count < nb_example and n_iter < n_iter_max):
            if (numpy.dot(datas[i], self.weights)) * train_data_transform[i,-1] < 0:
              self.weights += self.mu * train_data_transform[i,-1] * datas[i]
              count = 0
            else:
              count = count + 1
            i = (i + 1) % nb_example
            n_iter += 1

	def compute_predictions(self, test_data,type_transformation=-1):
          # application de la transformation des données
           test_data_transform = utilitaires.applyTranform(test_data,type=type_transformation)

           sorties = []
           for i in range(len(test_data_transform)):
             data = []
             for j in range(len(test_data_transform[i])):
               data.append(test_data_transform[i][j])
             data.append(1)
             sorties.append(numpy.dot(data, self.weights))
           return sorties