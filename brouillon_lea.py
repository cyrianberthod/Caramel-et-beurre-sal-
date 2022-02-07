def IA_aligne(joueur,n): #aligne le plus de pion au rang n, joueur = joueur joué par l'IA
    génération= [[noeud.name for noeud in fils] for fils in tree.ZigZagGroupIter(root, maxlevel=n)] #liste de valeurs de noeuds par liste de génération 
    possiblité=génération[n]
    Lfinie=[]
    Lmax=[]
    for matrice in possibilité :
        if partie_finie(matrice):
            Lfinie.append(matrice)
    if len(Lfinie)!=0:
        return(random.choice(Lfinie))
    return(random.choice(Lmax))
            
