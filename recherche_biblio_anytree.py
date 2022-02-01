#Connaître la branche donc est issu un noeud 
>>> udo  =  Nœud ( "Udo" ) 
>>> marc  =  Nœud ( "Marc" ,  parent = udo ) 
>>> lian  =  Nœud ( "Lian" ,  parent = marc ) 
>>> udo . ancêtres 
() 
>>> marc . ancêtres 
(Node('Udo'),) 
>>> lian . ancêtres 
(Node('Udo'), Node('Udo/Marc'))

#Savoir si le noeud a des enfants ou pas
>>> udo  =  Nœud ( "Udo" ) 
>>> marc  =  Nœud ( "Marc" ,  parent = udo ) 
>>> lian  =  Nœud ( "Lian" ,  parent = marc ) 
>>> udo . is_leaf 
Faux 
>>> marc . is_leaf 
False 
>>> lian . is_leaf 
Vrai

#exemple d'arbre 
from anytree import Node, RenderTree

root = Node(10)

level_1_child_1 = Node(34, parent=root)
level_1_child_2 = Node(89, parent=root)
level_2_child_1 = Node(45, parent=level_1_child_1)
level_2_child_2 = Node(50, parent=level_1_child_2)

for pre, fill, node in RenderTree(root):
    print("%s%s" % (pre, node.name))
