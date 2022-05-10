##Importations
import numpy as np
import matplotlib.pyplot as plt
import random as rd
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

def chg_joueur(joueur_local):
    if joueur_local==1:
        joueur_local=2
    else:
        joueur_local=1
    return joueur_local


def capture_cube(case, Plateau_local, joueur): #capture le cube en position case si cela est possible
    P=Plateau_local
    l,c=case
    positions_possibles=[]# récupère les coordonnées (i,j) de tout les endroits ou le joueur peut jouer un nouveau coup , en bordure!
    for position in coord_bordure:
        lp,cp=position #lp=ligne et cp=colonne du doublet dans position
        if P[lp,cp]==0 or P[lp,cp]==joueur:
             positions_possibles.append((lp,cp))
    if case in positions_possibles: #verifie que  la position est valide
        P[l,c]=-1 #on enlève le cube, -1=case vide
        return True
    return False

##Peut-on pousser ici ?
def poussepossible(vide): #renvoie liste des coorconnées des posi° où on peut pousser
    l,c = vide
    A=[(0,0),(0,4),(4,0),(4,4)] #listes des coord des angles
    if vide in A: #si le pion a été pris dans un angle : 2 possiblités
      return [(abs(l-4),c),(l,abs(4-c))] #on fixe l ou c
    L=[(l,0),(l,4),(0,c),(4,c)] #si le pion n'a pas été pris dans un angle : 4 posibilités
    L.remove(vide)  #on ne peut pas laisser le pion où on l'a pris
    return L

def pousseok(vide,case): #case = coordonnées de là où l'on veut pousser
    Lpos=poussepossible(vide) #liste des positions de pousse possibles
    for k in Lpos:
        if case==k:  #si l'endroit où le joueur veut poser est dans Lposs
            return True
    return False

## Pousse de la ligne ou de la colonne
def pousse(vide, case, Plateau_local, joueur):
    P = Plateau_local
    l,c = case #position de la case de pose
    lv,cv = vide #position de la case vide

    #décalage de la ligne ou de la colonne de pousse
    if l == lv:
        if c<cv:
            for k in range (cv,0,-1):
                P[l,k]=P[l,k-1]
        else : 
            for k in range (cv,4):
                P[l,k]=P[l,k+1]
    elif c == cv: #peut etre remplacer par else 
        if l < lv:
            for k in range (lv,0,-1):
                P[k,c]=P[k-1,c]
        else :
            for k in range (lv,4):
                P[k,c]=P[k+1,c]
    #le pion du joueur se retrouve à la position de pousse
    P[l,c] = joueur     

##fonction partie finie
def elem_identiques(list): #return True si la liste est constituée d'éléments identiques, false sinon.
   return list.count(list[0]) == len(list) #on compte le nombre d'occurence du premier element , si il est egal à la taille de la liste alors la liste est formée d'elements identiques

def partie_finie2(Plateau_local, joueur_local):
    P=Plateau_local
    adv=chg_joueur(joueur_local)
    V=0
    #colonnes gagnantes ?
    for c in range(5):
        colonne=[P[l,c] for l in range(5)]
        if colonne.count(adv)==5 : #le joueur a fait gagné l'adversaire, il a donc perdu
            return adv
        if colonne.count(joueur_local)==5: #le joueur a une colonne gagnante
            V+=1
    #lignes gagnantes ?
    for l in range(5):
        ligne=[P[l,c] for c in range(5)]
        if ligne.count(adv)==5 : #le joueur a fait gagné l'adversaire, il a donc perdu
            return adv
        if ligne.count(joueur_local)==5: #le joueur a une colonne gagnante
            V+=1
    #diagonales gagnantes ?
    diag_1=[P[k,k] for k in range (5)]
    if diag_1.count(adv)==5 : #le joueur a fait gagné l'adversaire, il a donc perdu
        return adv
    if diag_1.count(joueur_local)==5: #le joueur a une colonne gagnante
            V+=1
    diag_2=[P[4,0],P[3,1],P[2,2],P[1,3],P[0,4]]
    if diag_2.count(adv)==5 : #le joueur a fait gagné l'adversaire, il a donc perdu
        return adv
    if diag_2.count(joueur_local)==5: #le joueur a une colonne gagnante
            V+=1

    if V!=0:
        return joueur_local
    else: #personne n'a gagné
        return False


#----------------------------------l'IA------------------------------------------------------------------------
def explore_1tour(Plateau_local, joueur_local):
    all_possibilities=[]
    #choisi la case vide
    for vide in coord_bordure : 
        P_copie=np.copy(Plateau_local) #fonction np.copy permet une copie viable du plateau de jeu alors qu'un simple égale crée des interferences avec l'autre plateau
        if capture_cube(vide, P_copie, joueur_local):
           #choisi la case de pousse
            for case in coord_bordure:
               if pousseok(vide, case): 
                  P_copie2=np.copy(P_copie) #on crée un nv plateau par possibilité de pousse
                  pousse(vide,case,P_copie2,joueur_local)
                  all_possibilities.append(P_copie2) #ajoute le plateau virtuel une fois le coup joué
    return all_possibilities

def IA_aleatoire(Plateau_local, joueurIA):
    coup = rd.choice(explore_1tour(Plateau_local, joueurIA)) #choisit un terme 
    return coup

def poids_fenetre(fenetre, joueurIA, mode_IA): #joueurIA = celui qui joue au rg du plateau
# 1 : mode offensive 2: mode defensif
    poids= 0
    adv=chg_joueur(joueurIA)
    
    #commun quelque soit le mode de l'IA
    if fenetre.count(joueurIA) == 5: #l'IA a une ligne gagnante
        poids+= 100000              
    elif fenetre.count(adv) == 5: #l'adversaire gagne
            poids -=100000
                     
   #selon le mode de l'IA             
    if mode_IA==1:#plus l'IA aligne de pions plus la fenêtre a un poids élevé
        if fenetre.count(joueurIA) == 4 :
            poids += 40
        elif fenetre.count(joueurIA) == 3 :
            poids += 30
        elif fenetre.count(joueurIA) == 2 :
            poids +=20
        elif fenetre.count(joueurIA) == 1 :
            poids +=10

    elif mode_IA==2: #moins l'adversaire aligne de pions plus la fenêtre a un poids élevé
        if fenetre.count(adv) == 4 :
            poids += 10
        elif fenetre.count(adv) == 3 :
            poids += 20
        elif fenetre.count(adv) == 2 :
            poids += 30
        elif fenetre.count(adv) == 1 :
            poids +=40
                     
    return poids

def poids_plateau(Plateau_local, joueurIA, mode_IA):
    P=Plateau_local
    poids= 0
    #poids colonnes
    for c in range(5):
        colonne=[P[l,c] for l in range(5)] #la fenêtre = listes des valeurs sur la colonne c
        poids+=poids_fenetre(colonne,joueurIA, mode_IA)
    #poids lignes
    for l in range(5):
        ligne=[P[l,c] for c in range(5)]
        poids+=poids_fenetre(ligne,joueurIA, mode_IA)
    #poids diagonales
    diag_1=[P[k,k] for k in range (5)]
    poids+=poids_fenetre(diag_1,joueurIA, mode_IA)
    diag_2=[P[4,0],P[3,1],P[2,2],P[1,3],P[0,4]]
    poids+=poids_fenetre(diag_2,joueurIA, mode_IA)

    return poids

def prisepossible(Plateau_local, joueur_local): #peut etre plus logique d'appeler cette fonction "capture_possible" au vu de la fonction capture_cube)
    L=[]
    for coord in coord_bordure:
        if Plateau_local(coord)==joueur_local or Plateau_local(coord)==0:  #mettre les (coord) entre [] car on manipule matrice.
            L.append(coord)  
    return L 
                     
def coup_gagnant(Plateau_local, joueur_local): #est-ce que le coup va former un plateau gagnant ?
    for P in explore_1tour(Plateau_local, joueur_local):
        if partie_finie(P):
            return True
    return False

def dernier_noeud(Plateau_local, joueur_local):
    return coup_gagnant(Plateau_local, joueur_local) or coup_gagnant(Plateau_local, chg_joueur(joueur_local)) or len(prisepossible(Plateau_local)) == 0
#manque argument entrée "joueur_local" pour prise possible().
                     
def minimax(Plateau_local, profondeur, alpha, beta, joueur_local):
    prises_valides=prisepossible(Plateau_local, joueur_local)
    partie_terminée = dernier_noeud(Plateau_local, joueur_local)
    if profondeur == 0 or partie_terminée: 
        if partie_terminée:
            if coup_gagnant(Plateau_local, chg_joueur(joueur_local)):
                return (None, -100000000000000)
            elif coup_gagnant(Plateau_local,joueur_local):
                return (None, 10000000000000)
            else: #La partie est finie mais personne n'a gagné
                return (None, 0)
        else: #profondeur=0
            return (None, poids_plateau(Plateau_local, chg_joueur(joueur_local), 1))
    if joueur_local:
        max = -math.inf
        #vide = rd.choice(prises_valides)
        #case = rd.choice(poussepossible(vide))
        for vide in prises_valides:
            for case in poussepossible(vide):
                Pcopy = np.copy(Plateau_local)
                pousse(vide,case,Pcopy,joueur_local)
                nouveau_score = minimax(Pcopy, depth-1, alpha, beta, False)[1]  #modifier pour etre en accord avec arguments entrée fonction.
                if nouveau_score > max:
                    max = nouveau_score
                    coup = (vide,case)
               # alpha = max(alpha, value)
                #if alpha >= beta:
                  #  break
        return coup, max

    else: # Min player (avdersaire)
        min = math.inf
        for vide in prises_valides:
            for case in poussepossible(vide):
                Pcopy = np.copy(Plateau_local)
                pousse(vide,case,Pcopy,joueur_local)
                nouveau_score = minimax(Pcopy, depth-1, alpha, beta, True)[1]
                if nouveau_score < min:
                    min = nouveau_score
                    coup = (vide,case)
               # beta = min(beta, min)
                #if alpha >= beta:
                    #break
        return coup, max #return coup,min??

def minimax_cyrian(Plateau_local, profondeur, alpha, beta, joueur_local):
    
    prises=prisepossible(Plateau_local)

    #On commence par retourner le poids du plateau dans le cas ou on est au dernier rang
    if partie_finie2(Plateau_local, joueur_local)!=False or profondeur==0:
        return [None, poids_plateau(Plateau_local, joueur_local, 1)]

    #On est pas au dernier rang donc on appelle la fonction à la profondeur-1 (récursivité)    
    elif joueur_local==joueur: #on fait jouer le joueur virtuellement et on essaye de faire le meilleur coup possible
        max = -np.inf #moins l'infini 
        for vide in prises:
            for case in poussepossible(vide):
                Pcopy = np.copy(Plateau_local)
                pousse(vide,case,Pcopy,joueur_local) #joue le coup
                nouveau_score = minimax(Pcopy, profondeur-1, alpha, beta, chg_joueur(joueur_local))[1] #on prend que le poids et pas le coup
                if nouveau_score > max:
                    max = nouveau_score
                    coup = (vide,case)
                alpha = max(alpha, nouveau_score) 
                if alpha >= beta: #évite de calculer des branches inutilement 
                    break
        return [coup, max]
    
    else: #on fait jouer l'adversaire virtuellement et on essaye de faire le pire coup possible
        min = np.inf
        for vide in prises_valides:
            for case in poussepossible(vide):
                Pcopy = np.copy(Plateau_local)
                pousse(vide,case,Pcopy,joueur_local)
                nouveau_score = minimax(Pcopy, depth-1, alpha, beta, chg_joueur(joueur_local))[1] #on prend que le score et pas le coup
                if nouveau_score < min:
                    min = nouveau_score
                    coup = (vide,case)
                beta = min(beta, nouveau_score)
                if alpha >= beta:
                    break
        return [coup, min]


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
        testvide = np.where(Plateau == -1, 1,0) #renvoie une matrice avec des 1 là où il y a des -1 dans le plateau et des 0 sinon
        
        #Phase de capture
        if testvide==np.zeros((5,5)):
            print('capture')
            print(minimax_cyrian(Plateau, 3, -1000000, 1000000, joueur))
            capture_cube(case,Plateau,joueur)
            refresh()
                      
        
        #Phase de pousse
        else: #le cube à été capturé
            if pousseok(vide,case):
                pousse(vide,case,Plateau,joueur)
                print('pose')
                refresh()
                
                if partie_finie2(Plateau,joueur) != False: #si la partie est terminée
                    if partie_finie2(Plateau,joueur)==1:
                        gagnant="rond gagne"
                    else:
                        gagnant="croix gagne"

                    plt.text(1,-0.5,gagnant, fontsize=15, color='red')
                    
                else: #si la partie n'est pas finie
                    #changement de tour
                    joueur = chg_joueur(joueur)
    


fig.canvas.mpl_connect('button_press_event', clic)
plt.interactive(True) 
plt.pause(10000) #evite que la figure se ferme 
plt.show(block=False) #evite les bugs 
