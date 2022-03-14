def coup_gagnant(Plateau_choisi, joueur_choisi):
    for P in explore_1tour(Plateau_choisi, joueur_choisi):
        if partie_finie(P):
            return True
    return False

def chg_joueur(joueur_choisi):
    if joueur_choisi==1:
        joueur=2
    else:
        joueur=1
    return joueur

def minimax(Plateau_choisi, profondeur, alpha, beta, joueur_choisi):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, AI_PIECE):
				return (None, 100000000000000)
			elif winning_move(board, PLAYER_PIECE):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, AI_PIECE))
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

 
