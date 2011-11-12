# coding=utf-8
import numpy
import utilitaires

class classif_lineaire:
	def __init__(self, mu):
		self.mu = mu
    
	def train(self, train_data):
		# il faut ajouter le code ici.
		# Le code devrait etre tres similaire au perceptron mais le gradient devrait etre different
		# voir les notes sur la regression et sur LMS
		pass

	def compute_predictions(self, test_data,type_transformation):
		# il va falloir remplacer cette ligne
		sorties = numpy.random.randn(test_data.shape[0])
		
		return sorties
