import numpy as np
import matplotlib.pyplot as plt
import random as rd
import anytree as tree

M=np.zeros((5,5))
M2= np.array2string(M)

N=np.zeros((2,2))

root = tree.Node('racine', parent=None)

child1 = tree.Node(N, root) #l'important est que le deuxieme argument de la fontction Node soit lui meme un noeud et NON une matrice, un entier, une chaine de caract
child2 = tree.Node(N, child1)
child3 = tree.Node('enfant3', root)
child4 = tree.Node('petit fils teubé', child3)

print(tree.RenderTree(root).by_attr())
