#un site pas mal : https://anytree.readthedocs.io/en/1.0.1/api.html

import numpy as np
import matplotlib.pyplot as plt
import random as rd
import anytree as tree

M=np.zeros((5,5))
M2= np.array2string(M)

N=np.zeros((2,2))

root = tree.Node('racine', parent=None)

child1 = tree.Node('Dodo', root) #l'important est que le deuxieme argument de la fontction Node soit lui meme un noeud et NON une matrice, un entier, une chaine de caract
child2 = tree.Node('poussée à la ride', child1)
child3 = tree.Node('fils sain d esprit', root)
child4 = tree.Node('petit fils teubé', child3)
child4 = tree.Node('petit fils prodige',child3)

#_______________________________________afficher l'arbre___________________________________________________________________

arbre = tree.RenderTree(root).by_attr()
print(arbre)

#_________________parcourir l'arbre (extraire un chemin du noeud A au noeud B)___________________________________________________________________

w = tree.Walker() #Walker() est une class Anytree 
chemin = w.walk(root, child3)
#print(chemin)

#ou selon le rang des noeuds

chemin2 = [[noeud.name for noeud in fils] for fils in tree.ZigZagGroupIter(root, maxlevel=2)] #ZigZagGroupIter mais aussi PreOrderIter et PostOrderIter
chemin3 = [noeud.name for noeud in tree.PreOrderIter(root, maxlevel=4)]
chemin4 = [noeud.name for noeud in tree.PostOrderIter(root, maxlevel=4)]
#print(chemin2,'\n',chemin3,'\n',chemin4)
#________________________________extraire la variable d'un noeud quelquonque___________________________________________________________________

var = child2.name
#print(var)

