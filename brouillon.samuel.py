## comment integrer les diff IA dans la fonction clique
#une colonne joueur 1 ou on choisit joueur 1 parmis des IA ou joueur physique 
#.......joueur2.........joueur 2
#il faut donc faire une fonction click qui s'active au bout de 2 click 
#il faut passer par des classes pour faire cohabiter IA voir lien ci dessous pour comprendre
#https://kongakura.fr/article?id=Cr%C3%A9er_une_I.A_qui_apprend_toute_seule_%C3%A0_jouer_au_morpion


def liste_prises(Plateau):
    L=[]
    for coord in coord_bordure:
        if coord==joueur or coord==0:
            L.append(joueur)
    return L

def coup_gagnant(plateau,joueur):
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
    
