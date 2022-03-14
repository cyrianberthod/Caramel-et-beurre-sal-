## comment integrer les diff IA dans la fonction clique
#une colonne joueur 1 ou on choisit joueur 1 parmis des IA ou joueur physique 
#.......joueur2.........joueur 2
#il faut donc faire une fonction click qui s'active au bout de 2 click 
#il faut passer par des classes pour faire cohabiter IA voir lien ci dessous pour comprendre
#https://kongakura.fr/article?id=Cr%C3%A9er_une_I.A_qui_apprend_toute_seule_%C3%A0_jouer_au_morpion
def chg_joueur(joueur_choisi):
    if joueur_choisi==1:
        joueur=2
    else:
        joueur=1
    return joueur


def liste_prises(Plateau):
    L=[]
    for coord in coord_bordure:
        if coord==joueur or coord==0:
            L.append(joueur)
    return L

 def coup_gagnant(Plateau_choisi, joueur_choisi):
    for P in explore_1tour(Plateau_choisi, joueur_choisi):
        if partie_finie(P):
            return True
    return False

def dernier_noeud(plateau_choisi):
    return coup_gagnant(plateau_choisi, joueur) or coup_gagnant(plateau_choisi, chg_joueur(joueur_choisi)) or len(listes_prises) == 0
    
def minimax(plateau_choisi,profondeur,joueur_choisi):
    position_valides=listes_prises(plateau_choisi)
	partie_terminée = dernier_noeud(choisi)
	if profondeur == 0 or partie_terminée:
		if partie_terminée:
			if coup_gagnant(plateau_choisi, chg_joueur(joueur_choisi)):
				return (None, 100000000000000)
			elif coup_gagnant(plateau_choisi,joueur):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # profondeur=0
			return (None, poids_plateau(plateau_choisie, chg_joueur(joueur_choisi))
 

def minimax(plateau_choisi,profondeur,joueur_choisi):
    prises_valides=listes_prises(plateau_choisi)
	partie_terminée = dernier_noeud(choisi)
	if profondeur == 0 or partie_terminée:
		if partie_terminée:
			if coup_gagnant(plateau_choisi, chg_joueur(joueur_choisi)):
				return (None, 100000000000000)
			elif coup_gagnant(plateau_choisi,joueur):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # profondeur=0
			return (None, poids_plateau(plateau_choisie, chg_joueur(joueur_choisi))
   
	if joueur_choisi:
		max = -math.inf
		#vide = rd.choice(prises_valides)
        #case = rd.choice(poussepossible(vide))
		for vide in prises_valides:
            for case in poussepossible(vide):
                Pcopy = np.copy(Plateau)
			    pousse(vide,case,Pcopy,joueur_choisi)
			    nouveau_score = minimax(Pcopy, depth-1, alpha, beta, False)[1]
			    if nouveau_score > max:
				    max = nouveau_score
				    coup = (vide,case)
			    alpha = max(alpha, value)
			    if alpha >= beta:
				    break
		return coup, max

	else: # Min player (avdersaire)
		min = math.inf
		for vide in prises_valides:
            for case in poussepossible(vide):
                Pcopy = np.copy(Plateau)
			    pousse(vide,case,Pcopy,joueur_choisi)
			    nouveau_score = minimax(Pcopy, depth-1, alpha, beta, True)[1]
			    if nouveau_score < min:
				    min = nouveau_score
				    coup = (vide,case)
			    beta = min(beta, min)
			    if alpha >= beta:
				    break
		return coup, max

#modifs:
def minimax(plateau_choisi,profondeur,joueur_choisi):
    prises_valides=listes_prises(plateau_choisi)
	partie_terminée = dernier_noeud(plateau_choisi)
	if profondeur == 0 or partie_terminée:
		if partie_terminée:
			if coup_gagnant(plateau_choisi,joueur_choisi):
				return (None, 100000000000000)
			elif coup_gagnant(plateau_choisi,chg_joueur(joueur_choisi)):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # profondeur=0
			return (None, poids_plateau(plateau_choisie, chg_joueur(joueur_choisi))
    elif joueur_choisi:
		max = -math.inf
		
		for vide in prises_valides:
            for case in poussepossible(vide):
                Pcopy = np.copy(Plateau)
			    pousse(vide,case,Pcopy,joueur_choisi)
			    nouveau_score = minimax(Pcopy, depth-1, alpha, beta, False)[1]
			    if nouveau_score > max:
				    max = nouveau_score
				    coup = (vide,case)
			    alpha = max(alpha, value)
			    if alpha >= beta:
				    break
		return coup, max
