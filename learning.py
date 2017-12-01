#!/usr/bin/env python3

# Exécuter ce script pour (ré-)entrainer le modèle
# IMPORTANT : laisser la valeur de percentage à 1 dans jsonreader.py pour sauvegarder toutes les données
# Ne changer cette valeur que pour tester le modèle (exemple : 0.8 pour un ratio 80-20)

from open_json import *
from jsonreader import *
from make_dico import *
from sklearn import tree
import pickle

# initialistion liste de données global
features = []
targets = []
eval_features = []
eval_targets = []
eval_info = []
class_dict = dict()

# Chargement de la liste des nouveaux fichiers référence (dossier data)
json_files = json_path('data2')

# Parcours des fichiers
for file in json_files:

    # Construction des listes de données
    tmp_features, tmp_targets, tmp_info = make_data(file)
    tmp_eval_features, tmp_eval_targets, tmp_eval_info = make_test_data(file)

    # Construction du dictionnaire des classifications
    tmp_class_dict = make_dico_target_last(file)

    # update des liste de donnée global
    features.extend(tmp_features)
    targets.extend(tmp_targets)
    eval_features.extend(tmp_eval_features)
    eval_targets.extend(tmp_eval_targets)
    class_dict.update(tmp_class_dict)

# Uniformisation des listes (pour que les lignes aient toutes la même longueur)
features, eval_features = uniformise_features(features, eval_features)

# Construction de l'arbre de décision
model = tree.DecisionTreeClassifier()
model = model.fit(features, targets)

nb_error = 0

# Évaluation des données de test
for i in range(len(eval_features)):
    answer = model.predict([eval_features[i]])[0]
    check = eval_targets[i]
    if answer != check:
        print("Je pense que ce produit a pour catégorie... " + class_dict[answer])
        print("Le produit est en réalité dans la catégorie... " + class_dict[check])
        print("Le objet est l'id =" + eval_info[i]['id'] + "dans le fichier " + eval_info[i]['file'] + "\n")
        print("\033[91mERROR\033[0m\n")
        nb_error = nb_error + 1

# Pourcentage de précision de la machine
if len(eval_features) > 0:
    raw_precision = ((len(eval_features) - nb_error) / len(eval_features))*100
    precision = format(raw_precision, '.2f')
    print("Le pourcentage de précision est de \033[92m" + str(precision) + "%.\033[0m")
    print("Nombre d'erreurs : " + str(nb_error) + ".\n")

# Sauvegarde du modèle
else:
    pickle.dump(features, open('model/features.sav', 'wb'))
    pickle.dump(targets, open('model/targets.sav', 'wb'))
    pickle.dump(class_dict, open('model/class_dict.sav', 'wb'))
    print("Modèle sauvegardé.")
