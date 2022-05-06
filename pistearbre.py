#Pourquoi faire un arbre ? 
#but : déterminer toutes nos actions possibles pour les rangsmax coups prochains 

rangmax=1 #rang 1 = plateau actuel on rangmax-1 coups
root = tree.Node('racine')

def creaarbre(plateau_fils, noeud_parent, jlocal, k): #au premier appel creanoeud(Plateau,root,joueur,0)
    if k==rangmax or partie_finie(plateau_fils): #on s'arrête si on est arrivé au rang n (defini globalement) ou si la branche est finie
        return 
    else:
        #création du noeud fils
        fils=tree.Node(plateau_fils,noeud_parent)
        rg=explore_1tour(plateau_fils,jlocal) #liste des plateaux petit-fils
        #changement de tour dans l'IA
        if jlocal==1:
            jlocal=2
        else:
            jlocal=1
        #création des noeuds petit-fils
        for petit_fils in rg:
            creaarbre(petit_fils,fils,jlocal,k+1) #le petit-fils devient le fils, on avance d'un rang , au tour d'après le joueur doit être différent

#creaarbre(Plateau,root,joueur,0)
#print(tree.RenderTree(root).by_attr())
