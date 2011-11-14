# coding=utf-8

import numpy
import random
import pylab
import time
import perceptron_corrige as perceptron
import classif_lineaire_corrige as classif_lineaire
import utilitaires_corrige as utilitaires


def run_non_linear_data():
    # charger les donnees
    data = numpy.loadtxt('ellipse.txt')
    #data = numpy.loadtxt('cercle.txt')
    type_transformation=2

    # Les colonnes (traits/caracteristiques) sur lesqueles on va entrainer notre modele
    # Pour que gridplot fonctionne, len(train_cols) devrait etre 2
    train_cols = [0,1]
    # L'indice de la colonne contenant les etiquettes
    target_ind = [data.shape[1] - 1]

    # Nombre de classes
    n_classes = 2
    # Nombre de points d'entrainement
    n_train = 1500
    # Taille de la grille = grid_size x grid_size
    grid_size = 50

    print "On va entrainer un algo lineaire sur ", n_train, " exemples d'entrainement"

    # decommenter pour avoir des resultats non-deterministes 
    random.seed(3395)

    # Déterminer au hasard des indices pour les exemples d'entrainement et de test
    inds = range(data.shape[0])
    random.shuffle(inds)
    train_inds = inds[:n_train]
    test_inds = inds[n_train:]

    # separer les donnees dans les deux ensembles
    train_set = data[train_inds,:]
    train_set = train_set[:,train_cols + target_ind]
    test_set = data[test_inds,:]
    test_set = test_set[:,train_cols + target_ind]
    
    # separarer l'ensemble de test dans les entrees et les etiquettes
    test_inputs = test_set[:,:-1]
    test_labels = test_set[:,-1]
    
    mu = 0.0005
    #model = perceptron.perceptron(mu)
    model = classif_lineaire.classif_lineaire(mu)
    model.train(train_set,type_transformation)
    
    # Obtenir ses prédictions
    t1 = time.clock()
    les_sorties = model.compute_predictions(test_inputs,type_transformation)
    
    t2 = time.clock()
    print 'Ca nous a pris ', t2-t1, ' secondes pour calculer les predictions sur ', test_inputs.shape[0],' points de test'
    
    # Vote majoritaire (+1 puisquie nos classes sont de 1 a n)
    classes_pred = numpy.sign(les_sorties)
    
    # Faire les tests
    err = 1.0 - numpy.mean(test_labels==classes_pred)
    print "L'erreur de test est de ", 100.0 * err,"%"
    
    if len(train_cols) == 2:
        # Surface de decision
        t1 = time.clock()
        utilitaires.gridplot(model,train_set,test_set,n_points = grid_size,type_transformation=type_transformation)
        t2 = time.clock()
        print 'Ca nous a pris ', t2-t1, ' secondes pour calculer les predictions sur ', grid_size * grid_size, ' points de la grille'
        filename = 'grille_' + '_c1=' + str(train_cols[0]) + '_c2=' + str(train_cols[1])+'.png'
        print 'On va sauvegarder la figure dans ', filename
        pylab.savefig(filename,format='png')
        
    else:
        
        print 'Trop de dimensions (', len(train_cols),') pour pouvoir afficher la surface de decision'


def run_iris():
    # On commence par charger iris
    iris = numpy.loadtxt('iris.txt')
    data = iris
    type_transformation=-1

    # On se limite au cas de la classification BINAIRE donc on va seulement garder 
    # données des 2 premières classes.
    # Ici on garde juste les exemples avec l'etiquette 1 et 2.
    data = data[data[:,-1]<3,:]
    # Ici on transforme chaque etiquette qui est egale a 2 en -1, pour avoir les 
    # mêmes étiquettes que dans la formulation standard du perceptron (1 et -1).
    data[data[:,-1]==2,-1] = -1

    # On se limite à des données dont la dimension est 2, de façon à pouvoir visualiser
    # la frontirère de decision avec la fonction gridplot.
    train_cols = [2,3]
    # Une variable pour contenir l'indice de la colonne correspondant aux étiquettes.
    target_ind = [data.shape[1] - 1]

    # Nombre de classes
    n_classes = 2
    # Nombre de points d'entrainement
    n_train = 75
    # Taille de la grille = grid_size x grid_size
    grid_size = 50

    print "On va entrainer un classifieur sur ", n_train, " exemples d'entrainement"

    # decommenter pour avoir des resultats non-deterministes 
    random.seed(3395)

    # Déterminer au hasard des indices pour les exemples d'entrainement et de test
    inds = range(data.shape[0])
    random.shuffle(inds)
    train_inds = inds[:n_train]
    test_inds = inds[n_train:]
    
    # Separer les donnees dans les deux ensembles: entrainement et test.
    train_set = data[train_inds,:]	# garder les bonnes lignes
    train_set = train_set[:,train_cols + target_ind]  # garder les bonnes colonnes
    test_set = data[test_inds,:]
    test_set = test_set[:,train_cols + target_ind]

    # Separarer l'ensemble de test: entrees et etiquettes.
    test_inputs = test_set[:,:-1]
    test_labels = test_set[:,-1]

    # Le taux d'apprentissage
    mu = 0.005

    # Créer et entrainer le modele
    model = perceptron.perceptron(mu)
    #model = classif_lineaire.classif_lineaire(mu)
    model.train(train_set,type_transformation)

    # Obtenir les sorties sur l'ensemble de test.
    t1 = time.clock()
    les_sorties = model.compute_predictions(test_inputs,type_transformation)
    t2 = time.clock()
    print 'Ca nous a pris ', t2-t1, ' secondes pour calculer les predictions sur ', test_inputs.shape[0],' points de test'

    # Convertir les sorties en classe. On prend le signe.
    classes_pred = numpy.sign(les_sorties)
    
    # Mesurer la performance.
    err = 1.0 - numpy.mean(test_labels==classes_pred)
    print "L'erreur de test est de ", 100.0 * err,"%"

    # Affichage graphique
    if len(train_cols) == 2:
        # Surface de decision
        t1 = time.clock()
        utilitaires.gridplot(model,train_set,test_set,n_points = grid_size,type_transformation =type_transformation)
        t2 = time.clock()
        print 'Ca nous a pris ', t2-t1, ' secondes pour calculer les predictions sur ', grid_size * grid_size, ' points de la grille'
        filename = 'grille_' + '_c1=' + str(train_cols[0]) + '_c2=' + str(train_cols[1])+'.png'
        print 'On va sauvegarder la figure dans ', filename
        pylab.savefig(filename,format='png')
        
    else:
        print 'Trop de dimensions (', len(train_cols),') pour pouvoir afficher la surface de decision'

#run_iris()
run_non_linear_data()