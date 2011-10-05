# coding=utf-8

import numpy
import random
import pylab
import time
import parzen as parzen
import utilitaires

# charger iris
iris = numpy.loadtxt('iris.txt')
data = iris

# Les colonnes (traits/caracteristiques) sur lesqueles on va entrainer notre modele
# Pour que gridplot fonctionne, len(train_cols) devrait etre 2
train_cols = [0,1]
# L'indice de la colonne contenant les etiquettes
target_ind = [data.shape[1] - 1]

# Nombre de classes
n_classes = 3
# Nombre de points d'entrainement
n_train = 100
# Taille de la grille = grid_size x grid_size
grid_size = 100

print "On va entrainer un parzen sur ", n_train, " exemples d'entrainement"

# Commenter pour avoir des resultats non-deterministes 
random.seed(3395)
# Determiner au hasard des indices pour les exemples d'entrainement et de test
inds = range(data.shape[0])
random.shuffle(inds)
train_inds = inds[:n_train]
test_inds = inds[n_train:]

# Separer les donnees dans les deux ensembles
train_set = data[train_inds,:]
train_set = train_set[:,train_cols + target_ind]
test_set = data[test_inds,:]
test_set = test_set[:,train_cols + target_ind]

# Separarer l'ensemble de test dans les entrees et les etiquettes
test_inputs = test_set[:,:-1]
test_labels = test_set[:,-1]

# Créer le classifieur
model = parzen.parzen(n_classes)

# L'entrainer
model.train(train_set)

# Obtenir ses predictions
t1 = time.clock()
les_comptes = model.compute_predictions(test_inputs)
t2 = time.clock()
print 'Ca nous a pris ', t2-t1, ' secondes pour calculer les predictions sur ', test_inputs.shape[0],' points de test'

# Vote majoritaire (+1 puisque nos classes sont de 1 a n)
classes_pred = numpy.argmax(les_comptes,axis=1)+1

# Faire les tests
# Matrice de confusion 
confmat = utilitaires.teste(test_labels, classes_pred)
print 'La matrice de confusion est:'
print confmat

# Erreur de test
sum_preds = numpy.sum(confmat)
sum_correct = numpy.sum(numpy.diag(confmat))
print "L'erreur de test est de ", 100*(1.0 - (float(sum_correct) / sum_preds)),"%"

# Affichage
if len(train_cols) == 2:
    # Surface de decision
    t1 = time.clock()
    utilitaires.gridplot(model,train_set,test_set,n_points = grid_size)
    t2 = time.clock()
    print 'Ca nous a pris ', t2-t1, ' secondes pour calculer les predictions sur ', grid_size * grid_size, ' points de la grille'
    #filename = 'grille_' + '_k=' + str(k) + '_c1=' + str(train_cols[0]) + '_c2=' + str(train_cols[1])+'.png'
    #print 'On va sauvegarder la figure dans ', filename
    #pylab.savefig(filename,format='png')
else:
    print 'Trop de dimensions (', len(train_cols),') pour pouvoir afficher la surface de decision'