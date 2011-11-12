# coding=utf-8
import numpy
import utilitaires

class perceptron:
	def __init__(self, mu):
		self.mu = mu
    
	def train(self, train_data,type_transformation=-1):
		print train_data.shape

		#on initialise les poids avec un exemple aleatoire de notre train set
		self.weights = numpy.random.random(train_data.shape[1])
		self.weights[-1] = 0

		# il faut appliquer une transformation non-lineaire ici pour rendre le data lineairement separable. On peut ecrire une fonction qui fait ceci et l'appeler d'ici.
		datas = numpy.array(train_data)
		datas[:,-1] = 1
		i = 0
		count = 0 
		n_iter = 0
		n_iter_max = train_data.shape[0]*10 #on permet maximum 10 epoque d'entrainement pour limiter les calculs
		while (count < train_data.shape[0] and n_iter < n_iter_max):
			if (numpy.dot(datas[i], self.weights)) * train_data[i,-1] < 0:
				self.weights += self.mu * train_data[i,-1] * datas[i]
				count = 0
			else:
				count = count + 1
			i = (i + 1) % train_data.shape[0]
			n_iter += 1

	def compute_predictions(self, test_data,type_transformation):
		sorties = []
		# il faut appliquer une transformation non-lineaire ici pour rendre le data lineairement separable. On peut ecrire une fonction qui fait ceci et l'appeler d'ici.
		for i in range(len(test_data)):
			data = []
			for j in range(len(test_data[i])):
				data.append(test_data[i][j])
			data.append(1)
			sorties.append(numpy.dot(data, self.weights))
		return sorties
