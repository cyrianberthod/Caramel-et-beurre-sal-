##Importations
import numpy as np
import matplotlib.pyplot as plt
import random as rd
import anytree as tree
#on pose l=ligne et c=colonne
#Joueur 1 = croix , Joueur 2 = rond
coord_bordure=[(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (1, 0), (2, 0), (3, 0), (1, 4), (2, 4), (3, 4)]

#------------------------------------------------Matrice-------------------------------------------------------------------------------

#initialiation
def play():
    global Plateau
    Plateau=np.zeros((5,5))
    global joueur
    joueur = rd.randint(1,2) #le joueur 1 ou le joueur 2 commence (hasard)

play()


def capture_cube(case, Plateau_choisi, joueur): #capture le cube en position case si cela est possible
    P=Plateau_choisi
    l,c=case
    positions_possibles=[]# récupère les coordonnées (i,j) de tout les endroits ou le joueur peut jouer un nouveau coup , en bordure!
    for position in coord_bordure:#lp=ligne du doublet dans position cp=colonne du doublet dans position
        lp,cp=position
        if P[lp,cp]==0 or P[lp,cp]==joueur:
             positions_possibles.append((lp,cp))
    if case in positions_possibles: #verifie que  la position est valide
        P[l,c]=-1 #on enlève le cube, -1=case vide
        #print(P)
        return True
    return False

##Peut-on pousser ici ?
def poussepossible(vide): #renvoie liste des coorconnées des posi° où on peut pousser
    l,c = vide
    A=[(0,0),(0,4),(4,0),(4,4)] #listes des coord des angles
    if vide in A: #si le pion a été pris dans un angle
      return [(abs(l-4),c),(l,abs(4-c))]#on fixe l ou c , on determine les endroits ou on peut pousser par la relation avec la valeur absolue abs() (faire dessin)
    L=[(l,0),(l,4),(0,c),(4,c)] #si le pion n'a pas été pris dans un angle 4 posibilités
    L.remove(vide)  #on ne peut pas laisser le pion où on l'a pris
    return L

def pousseok(vide,case): #case = coordonnées de là où on veut pousser
    Lpos=poussepossible(vide) #liste des positions de pousse possibles
    for k in Lpos:
        if case==k:  #l'endroit où le joueur veut poser est dans Lposs => c ok
            return True
    return False

## Pousse de la ligne ou de la colonne
def pousse(vide, case, Plateau_choisi, joueur):
    P = Plateau_choisi
    l,c = case #position de la case de pose
    lv,cv = vide #position de la case vide

    #décalage de la ligne ou de la colonne de pousse
    if l == lv:
        if c<cv:
            for k in range (cv,0,-1):
                P[l,k]=P[l,k-1]
        elif c > cv: #peut etre remplacer par else si impossible de poser au même endroit
            for k in range (cv,4):
                P[l,k]=P[l,k+1]
    elif c == cv: #peut etre remplacer par else 
        if l < lv:
            for k in range (lv,0,-1):
                P[k,c]=P[k-1,c]
        elif l > lv: #peut etre remplacer par else si impossible de poser au même endroit
            for k in range (lv,4):
                P[k,c]=P[k+1,c]
    #pose du cube à la position de pousse
    P[l,c] = joueur     
    #print(P)

##fonction partie finie
def check(list): 
   return list.count(list[0]) == len(list) #on compte le nombre d'occurence du premier element , si il est egal à la taille de la liste alors la liste est formée d'elements identiques

def partie_finie(Plateau_choisi):
    P=Plateau_choisi
    coord_ligne_haut=[(0,k) for k in range (5)]
    coord_colonne_gauche=[(k,0) for k in range (5)]
    coord_diag_1=[(k,k) for k in range (5)]
    coord_diag_2=[(4,0),(3,1),(2,2),(1,3),(0,4)]
    V=[]
    for coord in coord_ligne_haut: #une colonne gagnante? #pourquoi ne pas remplacer par un simple compteur?
        bin,c=coord
        colonne=[P[k,c] for k in range(5)] #on recupère les données de chaque colonne 
        if check(colonne) and colonne[0]!=0: #la fonction check() renvoie True si les elements d'une liste sont identiques
            V.append([True,colonne[0]])
    for coord in coord_colonne_gauche: #une ligne gagnante? #pourquoi ne pas remplacer par un simple compteur?
        l,bin=coord
        ligne=[P[l,k] for k in range(5)]
        if check(ligne) and ligne[0]!=0:
            V.append([True,ligne[0]])
    diag_1=[P[coord] for coord in coord_diag_1]
    diag_2=[P[coord] for coord in coord_diag_1]
    if check(diag_1) and diag_1[0]!=0 : #la premiere diagonale gagnante?
        V.append([True,diag_1[0]])
    elif check(diag_2) and diag_2[0]!=0: #la 2ème diagonale gagnante?
        V.append([True,diag_2[0]])
    return V
def partie_finie_optimisee(Plateau_choisi):
    P=Plateau_choisi
    V=[]
    for c in range(5):
        colonne=[P[k,c] for k in range(5)] #on recupère les données de chaque colonne
        if check(colonne) and colonne[0]!=0: #la fonction check() renvoie True si les elements d'une liste sont identiques
            V.append([True,colonne[0]])
    for l in range(5):
        ligne=[P[l,k]  for k in range(5)]
        if check(ligne) and ligne[0]!=0:
            V.append([True,ligne[0]])
    diag_1=[P[(k,k)] for k in range(5)]
    diag_2=[P[coord] for coord in [(4,0),(3,1),(2,2),(1,3),(0,4)]]
    if check(diag_1) and diag_1[0]!=0 : #la premiere diagonale gagnante?
        V.append([True,diag_1[0]])
    elif check(diag_2) and diag_2[0]!=0: #la 2ème diagonale gagnante?
        V.append([True,diag_2[0]])
    return V
def partie_finie2(plateau, joueur):
    adv=chg_joueur(joueur)
    if joueur==1:
        adv=2
        victoire_adv= "Les ronds ont gagné"
        victoire_joueur= "Le croix ont gagné"
    else:
        adv=1
        victoire_adv= "Les croix ont gagné"
        victoire_joueur= "Les ronds ont gagné"
    V=0
    #colonnes gagnantes ?
    for c in range(5):
        colonne=[plateau[l,c] for l in range(5)]
        if colonne.count(adv)==5 : #le joueur a fait gagné l'adversaire, il a donc perdu
            return victoire_adv
        if colonne.count(joueur)==5: #le joueur a une colonne gagnante
            V+=1
    #colonnes gagnantes ?
    for l in range(5):
        ligne=[plateau[l,c] for c in range(5)]
        if ligne.count(adv)==5 : #le joueur a fait gagné l'adversaire, il a donc perdu
            return victoire_adv
        if ligne.count(joueur)==5: #le joueur a une colonne gagnante
            V+=1
    #diagonales gagnantes ?
    diag_1=[plateau[k,k] for k in range (5)]
    if diag_1.count(adv)==5 : #le joueur a fait gagné l'adversaire, il a donc perdu
        return victoire_adv
    if diag_1.count(joueur)==5: #le joueur a une colonne gagnante
            V+=1
    diag_2=[plateau[4,0],plateau[3,1],plateau[2,2],plateau[1,3],plateau[0,4]]
    if diag_2.count(adv)==5 : #le joueur a fait gagné l'adversaire, il a donc perdu
        return victoire_adv
    if diag_2.count(joueur)==5: #le joueur a une colonne gagnante
            V+=1

    if V!=0:
        return victoire_joueur
    else: #personne n'a gagné
        return False

#----------------------------------l'IA------------------------------------------------------------------------
def explore_1tour(Plateau_choisi, joueur):
    all_possibilities=[]
    #choisi la case vide
    for l in range(5): #pourquoi pas faire un for coord in coord_bordure , on gagnerait du temps de calcul à l'ordi
        for c in range(5): 
            P_copie=np.copy(Plateau_choisi) #fonction np.copy permet une copie viable du plateau de jeu alors qu'un simple égale crée des interferences avec l'autre plateau
            vide = (l,c)
            if capture_cube(vide, P_copie, joueur):
                #choisi la case de pousse
                for i in range(5): #pourquoi pas faire un for coord in coord_bordure , on gagnerait du temps de calcul à l'ordi
                    for j in range(5):
                        case = (i,j)
                        P_copie2=np.copy(P_copie) #on crée un nv plateau par possibilité de pousse
                        if pousseok(vide, case): 
                            pousse(vide,case,P_copie2,joueur)
                            all_possibilities.append(P_copie2) #ajoute le plateau virtuel une fois le coup joué
    return all_possibilities


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

def IA_aleatoire(Plateau_choisi):
    coup = rd.choice(explore_1tour)
    return coup

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


def liste_prises(Plateau):
    L=[]
    for coord in coord_bordure:
        if coord==joueur or coord==0:
            L.append(joueur)
    return L

def dernier_noeud(plateau_choisi, joueur_choisi):
    return coup_gagnant(plateau_choisi, joueur_choisi) or coup_gagnant(plateau_choisi, chg_joueur(joueur_choisi)) or len(liste_prises(plateau_choisi)) == 0

def poids_fenetre(fenetre, joueurIA, mode_IA): #joueur = celui qui joue au rg du plateau = celui dont l'act° a formé ce plateau
# 1 : mode offensive 2: mode defensif
    poids= 0
    adv=chg_joueur(joueurIA)

    if fenetre.count(joueurIA) == 5: #le joueur a une ligne gagnante
        poids+= 1000

    if mode_IA==1:
        if fenetre.count(adv) == 5: #le joueur adverse gagne
            poids -=1000
        elif fenetre.count(joueurIA) == 4 :
            poids += 40
        elif fenetre.count(joueurIA) == 3 :
            poids += 30
        if fenetre.count(joueurIA) == 2 :
            poids +=20
        if fenetre.count(joueurIA) == 1 :
            poids +=10

    elif mode_IA==2:
        if fenetre.count(adv) == 5: #l'adversaire gagne
            poids -= 1000
        elif fenetre.count(joueurIA) == 4 :
            poids += 10
        elif fenetre.count(joueurIA) == 3 :
            poids += 20
        if fenetre.count(joueurIA) == 2 :
            poids +=30
        if fenetre.count(joueurIA) == 1 :
            poids +=40
    return poids

def poids_plateau(plateau, joueurIA, mode_IA):
    poids= 0
    #poids colonnes
    for c in range(5):
        colonne=[plateau[l,c] for l in range(5)] #la fenêtre = listes des valeurs sur la colonne c
        poids+=poids_fenetre(colonne,joueurIA, mode_IA)
    #poids lignes
    for l in range(5):
        ligne=[plateau[l,c] for c in range(5)]
        poids+=poids_fenetre(ligne,joueurIA, mode_IA)
    #poids diagonales
    diag_1=[plateau[k,k] for k in range (5)]
    poids+=poids_fenetre(diag_1,joueurIA, mode_IA)
    diag_2=[plateau[4,0],plateau[3,1],plateau[2,2],plateau[1,3],plateau[0,4]]
    poids+=poids_fenetre(diag_2,joueurIA, mode_IA)

    return poids

def minimax(plateau_choisi,profondeur,joueur_choisi):
    prises_valides=liste_prises(plateau_choisi)
    partie_terminée = dernier_noeud(plateau_choisi, joueur_choisi)
    if profondeur == 0 or partie_terminée:
        if partie_terminée:
            if coup_gagnant(plateau_choisi, chg_joueur(joueur_choisi)):
                return (None, 100000000000000)
            elif coup_gagnant(plateau_choisi,joueur_choisi):
                return (None, -10000000000000)
            else: # Game is over, no more valid moves
                return (None, 0)
        else: # profondeur=0
            return (None, poids_plateau(plateau_choisi, chg_joueur(joueur_choisi), 1))
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


#------------------------------------------------------Interface Graphique-----------------------------------------------------------

##figure 
#xc,yc correspont au sommet bas gauche de chaque case dans le graphique
fig = plt.figure()
ax = plt.axes(aspect=1) #repère orthonormé
plt.xlim(-4,9) 
plt.ylim(-1,6)
plt.axis('off')
plt.title('QUIXO')
contour = plt.Rectangle((-1,-1),7,7,fc=(0.8,0.8,0.8)) #fc=face colour : couleur de ce qu'on trace
fond = plt.Rectangle((-4,-1),13,7,fc=(0.5,0.5,0.5))
ax.add_patch(fond)
ax.add_patch(contour)
fond_plateau = plt.Rectangle((0,0),5,5, fc=(0.4,0.25,0.2))
ax.add_patch(fond_plateau)

#boutons
bouton_newgame=plt.Rectangle((1,5.2),3,0.6,fc='black') #bouton new game
ax.add_patch(bouton_newgame)
text_newgame=plt.text(2.5,5.5,'New Game',fontsize=8,horizontalalignment='center',verticalalignment='center',color='w')

text_joueur1=plt.text(-2.5,5.5,'Joueur 1',fontsize=12,horizontalalignment='center',verticalalignment='center',color='black')
text_joueur2=plt.text(7.5,5.5,'Joueur 2',fontsize=12,horizontalalignment='center',verticalalignment='center',color='black')

for i in [-3.5,6.5]:
    for j in range (4,0,-1):
        b=plt.Rectangle((i,j),2,0.6,fc='black')
        ax.add_patch(b)
for i in [-2.5,7.5]:
    text_utilisateur=plt.text(i,4.3,'utilisateur',fontsize=8,horizontalalignment='center',verticalalignment='center',color='white')
    text_IArand=plt.text(i,3.3,'IA aleatoire',fontsize=8,horizontalalignment='center',verticalalignment='center',color='white')
    text_IAoff=plt.text(i,2.3,'IA offensive',fontsize=8,horizontalalignment='center',verticalalignment='center',color='white')
    text_IAdef=plt.text(i,1.3,'IA defensive',fontsize=8,horizontalalignment='center',verticalalignment='center',color='white')



for k in range (-1,5): #grille
    h=k+0.975
    lignev = plt.Rectangle((h,0),0.05,5,fc=(0.8,0.8,0.8))
    ligneh = plt.Rectangle((0,h),5,0.05,fc=(0.8,0.8,0.8))
    ax.add_patch(lignev)
    ax.add_patch(ligneh)


##mise à jour de la figure en fonction de la matrice
def refresh(): 
    P=Plateau
    neutre=[]
    croix=[]
    rond=[]
    global vide #nécessaire pour pour l'appeler dans clic
    for l in range(5):
        for c in range(5):
            case=(l,c)
            if P[l,c]==0:
                neutre.append(case)
    
            elif P[l,c]==1:
                croix.append(case)
            
            elif P[l,c]==2:
              rond.append(case)
    
            elif P[l,c]==-1:
                vide = case #pas besoin de liste, maximum une case vide
                yc, xc = vide 
                yc = 4-yc #passage de la matrice a la figure
                dessinvide = plt.Rectangle((xc,yc), width=1, height=1, facecolor=(0.8,0.8,0.8)) #width=largeur et height=longueur
                ax.add_patch(dessinvide)
    
    for cube in croix:
        yc, xc = cube
        yc = 4-yc #passage de la matrice a la figure
        dessinneutre = plt.Rectangle((xc+0.025,yc+0.025), width=0.95, height=0.95, facecolor=(0.4,0.25,0.2))
        ax.add_patch(dessinneutre)
        branche1 = plt.Rectangle((xc+0.25,yc+0.35), width=0.1, height=0.6, angle=-45, facecolor='black') # croix= 2 rectangles avec angle 45°
        branche2 = plt.Rectangle((xc+0.65,yc+0.3), width=0.1, height=0.6, angle=45, facecolor='black')
        ax.add_patch(branche1)
        ax.add_patch(branche2)
    for cube in rond:
        yc, xc = cube
        yc = 4-yc #passage de la matrice a la figure
        dessinneutre = plt.Rectangle((xc+0.025,yc+0.025), width=0.95, height=0.95, facecolor=(0.4,0.25,0.2))
        ax.add_patch(dessinneutre)
        dessinrond = plt.Circle((xc+0.5,yc+0.5), radius=0.3, facecolor='black')
        ax.add_patch(dessinrond)
    for cube in neutre:
        yc, xc = cube
        yc = 4-yc #passage de la matrice a la figure
        dessinneutre = plt.Rectangle((xc+0.025,yc+0.025), width=0.95, height=0.95, facecolor=(0.4,0.25,0.2))
        ax.add_patch(dessinneutre)


##actions declenchées par le clique de souris 
def clic(event):
    global joueur
    x,y = event.xdata,event.ydata #récupère les coord du clique
    

    #Connexion du bouton "new game"
    if 1<x<4 and 5.2<y<5.8:
        play()
        refresh()
        ax.texts=[ax.texts[k] for k in range(11)] #supprime les textes defini apres les 11 initiaux 
    
    #Au cours d'une partie
    else:
        c = int(x-x%1) #passage de la figure à la matrice
        l = int(4-(y-y%1))
        case = (l,c)
        testvide = np.where(Plateau == -1)[0] #renvoie une liste d'indices où les conditions ont été remplies
        
        #Phase de capture
        if testvide.size == 0: #vérifie que aucun cube n'a deja été sélectioné
            print('capture')
            creaarbre(Plateau,root,joueur,0)
            #print(tree.RenderTree(root).by_attr())
            print(minimax(Plateau, 10, joueur))
            capture_cube(case,Plateau,joueur)
            refresh()
                      
        
        #Phase de pousse
        else: #le cube à été capturé
            if pousseok(vide,case):
                pousse(vide,case,Plateau,joueur)
                print('pose')
                refresh()
                
                if len(partie_finie(Plateau))>0: # if partie finie = True (la fct° renvoie une 2-liste avec pour 1er terme un booléen)
                    V=partie_finie(Plateau)
                    gagnant=[elem[1] for elem in V] # le 2ème terme est le numéro du gagnant
                    if all(gagnant)==1 or all(gagnant)==2 : #s'il n'y a qu'un gagnant 
                        if V[0][1]==1:   # si le numéro ayant gagné est 1
                            gagnant="croix gagne"
                        else:
                            gagnant="rond gagne"
                        plt.text(1,-0.5,gagnant, fontsize=15, color='red')
                    else :  
                                                          
                        # s'il y a plusieurs gagnants c'est que le joueur a fait gagné sont adv
                        if joueur==1:
                            gagnant="rond gagne"
                        else:
                             gagnant="croix gagne"

                        plt.text(1,-0.5,gagnant, fontsize=15, color='red')
                    
                else: #si la partie n'est pas finie
                    #changement de tour
                    if joueur==1:
                        joueur=2
                    else:
                        joueur=1
    


fig.canvas.mpl_connect('button_press_event', clic)
plt.interactive(True) 
plt.pause(10000) #evite que la figure se ferme 
plt.show(block=False) #evite les bugs 
