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
            
def IA_aligne(joueur,n): #aligne le plus de pion au rang n, joueur = joueur joué par l'IA
    génération= [[noeud.name for noeud in fils] for fils in tree.ZigZagGroupIter(root, maxlevel=n)] #liste de valeurs de noeuds par liste de génération 
    possiblité=génération[n]
    Lfinie=[]
    for matrice in possibilité :
        if partie_finie(matrice): #la chemin aboutit à la victoire au rang n = c'est le meilleur chemin possible 
            Lfinie.append(matrice)
    if len(Lfinie)!=0: #s'il y a 1 ou plusieurs chemin menant à la victoire on en prend un aléatoirement 
        choix=random.choice(Lfinie)
        w = tree.Walker() 
        chemin = w.walk(root, choix) 
        chemin[2]       #renvoie qq de la forme (Node('/racine/fils sain d esprit'),)
        
    return(random.choice(Lfinie))
