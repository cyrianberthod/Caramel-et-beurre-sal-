def IA_aligne(joueur,n): #aligne le plus de pion au rang n, joueur = joueur joué par l'IA
    génération= [[noeud.name for noeud in fils] for fils in tree.ZigZagGroupIter(root, maxlevel=n)] #liste de valeurs de noeuds par liste de génération 
    possiblité=génération[n]
    Lfinie=[]
    option_max=0
    nbmax=0 #nombre de pions maximums alignés 
    for k in range(possibilité) :
        if partie_finie(possibilité[k]): #la chemin aboutit à la victoire au rang n = c'est le meilleur chemin possible 
            Lfinie.append(possibilité[k])
        else:
            if aligne(possibilité[k],joueur)>nbmax: #on cherche la matrice pour laquelle il y a le plus de pions alignés
                option_max=possibilité[k]
                nb=aligne(possibilité[k],joueur)
    if len(Lfinie)!=0: #s'il y a 1 ou plusieurs chemin menant à la victoire on en prend un aléatoirement 
        choix=random.choice(Lfinie)
    else:   #si aucun chemin ne mène à la victoire on choisit celui grace auquel l'IA aligne le plus de pions 
        choix=option_max 
    #on cherche le chemin à prendre pour aller vers le choix 
    w = tree.Walker() 
    chemin = w.walk(root, choix)   
    return(chemin[2]) # PROBLEME : renvoie qq de la forme (Node('/racine/fils sain d esprit'),) => on voudrait la valeur de l'étape 2 du chemin (ce que l'IA doit jouer à ce tour)
                        # child.ancestor[0].name
def IA_defencif(joueur,n): #aligne le plus de pion au rang n, joueur = joueur joué par l'IA
    if joueur=1:
        adv=2
    else:
        adv=1
    génération= [[noeud.name for noeud in fils] for fils in tree.ZigZagGroupIter(root, maxlevel=n)] #liste de valeurs de noeuds par liste de génération 
    possiblité=génération[n]
    option_min=0
    nbmin=0 #nombre de pions minimum alignés par l'adversaire  
    for k in range(possibilité) :
        if aligne(possibilité[k],adv)<nbmax: #on cherche la matrice pour laquelle il y a le plus de pions alignés
                Lmin=possibilité[k]
                nb=aligne(possibilité[k],joueur)
    choix=option_min
    #on cherche le chemin à prendre pour aller vers le choix 
    w = tree.Walker() 
    chemin = w.walk(root, choix)   
    return(chemin[2]) # PROBLEME : renvoie qq de la forme (Node('/racine/fils sain d esprit'),) => on voudrait la valeur de l'étape 2 du chemin (ce que l'IA doit jouer à ce tour)


def aligne(matrice,joueur): #on cherche à savoir le nbre max de pions du joueur sur un même ligne ou colonne ou diagonale 
    coord_ligne_haut=[(0,k) for k in range (5)]
    coord_colonne_gauche=[(k,0) for k in range (5)]
    coord_diag_1=[(k,k) for k in range (5)]
    coord_diag_2=[(4,0),(3,1),(2,2),(1,3),(0,4)]
    nb=0
    for coord in coord_ligne_haut: #nbre de pions sur les différentes colonnes
        bin,c=coord
        colonne=[matrice[k,c] for k in range(5)] #on recupère les données de chaque colonne 
        if colonne.count(joueur)>nb:
            nb=colonne.count(joueur) #on garde le nombre de pions sur la colonne qui en possède le plus 
    for coord in coord_colonne_gauche: #idem pour les lignes
        l,bin=coord
        ligne=[matrice[l,k] for k in range(5)]
        if ligne.count(joueur)>nb:
                nb=ligne.count(joueur)
    diag_1=[matrice[coord] for coord in coord_diag_1] #idem pour les diagonales 
    if diag_1.count(joueur)>nb:
        nb=colonne.count(joueur)
    diag_2=[matrice[coord] for coord in coord_diag_1]
    if diag_2.count(joueur)>nb:
        nb=colonne.count(joueur)   
    return nb 
