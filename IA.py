#pip install anytree   #si vous ne l'avais pas encore fait 
from anytree import Node

def creanoeud(parent,k): #au premier appel on creanoeud(parent,0)
    if k==n or rg=explore_1tour(parent)==[]: #on s'arrête si on est arrivé au rang n (defini globalement) ou si la branche est finie
        return
    else:
        rg=explore_1tour(parent)
        for element in rg:
            N=Node(element, parent)
            creanoeud(element,k+1) #l'élèment devient le parent, on avance d'un rang 
