#!/usr/bin/env python3
from open_json import *
from jsonreader import *
from make_dico import *
from sklearn import tree

# initialistion liste de données global
features = []
targets = []
test_data = []
check_data = []
class_dict = dict()
# Chargement de la liste des fichiers
json_files = json_path('data')

# Parcours des fichiers
for file in json_files:

    # Construction des listes de données
    # TODO: modifier cette partie du code pour construire UNE seule liste commune combinant les données de TOUS les fichiers, pour les 4 types de liste.
    tmp_features, tmp_targets, tmp_test_data, tmp_check_data = make_test_data(file)


    # Construction du dictionnaire des classifications
    # TODO: même chose que pour les listes de données, un seul dictionnaire commun.
    tmp_class_dict = make_dico(file)

    # update des liste de donnée global
    features.extend(tmp_features)
    targets.extend(tmp_targets)
    test_data.extend(tmp_test_data)
    check_data.extend(tmp_check_data)
    class_dict.update(tmp_class_dict)
features, test_data = uniformise_features(features, test_data)
# Construction de l'arbre de décision
clf = tree.DecisionTreeClassifier()
clf = clf.fit(features, targets)

# Évaluation des données de test
for i in range(len(test_data)):
    answer = clf.predict([test_data[i]])[0]
    check = check_data[i]
    print("Je pense que ce produit a pour catégorie... " + class_dict[answer])
    print("Le produit est en réalité dans la catégorie... " + class_dict[check])
    if answer != check:
        # TODO: intercepter les erreurs et calculer le pourcentage de précision de la machine.
        print("\033[91mERROR\033[0m")