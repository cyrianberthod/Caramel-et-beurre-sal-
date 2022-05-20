##Importations
import numpy as np
import random as rd
import matplotlib.pyplot as plt
import time

##Définition des variables globales 
#correspondance objet/matrice
croix=1
rond=2
indetermine=0
vide=-1
    
def chg_joueur(joueur_local):
    if joueur_local==croix:
        joueur_local=rond
    else:
        joueur_local=croix
    return joueur_local
    
#choix de la taille du plateau 
n=10

##Mise en place du jeu 

def play():
    global Plateau
    Plateau=np.zeros((n,n))
    global joueur
    joueur = rd.randint(croix,rond) #le joueur 1 ou le joueur 2 commence (hasard)
play()

def set_coord_bordure():
    L1=[(0,k) for k in range(n)]
    L2=[(n-1,k) for k in range(n)]
    L3=[(k,0) for k in range(1,n-1)]
    L4=[(k,n-1) for k in range(1,n-1)]
    L=L1+L2+L3+L4
    return L
coord_bordure=set_coord_bordure() 
#Peut-on effectueur l'action ?

def capture_possible(Plateau_local, joueur_local):
    L=[]
    for coord in coord_bordure:
        if Plateau_local[coord]==joueur_local or Plateau_local[coord]==indetermine:  
            L.append(coord)  
    return L 
    
def poussepossible(coord_vide): #renvoie liste des coordonnées des positions où l'on peut pousser à partir de l'emplacement de capture du pion
    l,c = coord_vide
    A=[(0,0),(0,n-1),(n-1,0),(n-1,n-1)] #coordonnées des angles
    if coord_vide in A: #si le pion a été pris dans un angle : 2 possiblités
      return [(abs(l-(n-1)),c),(l,abs((n-1)-c))] #on fixe l ou c
    L=[(l,0),(l,n-1),(0,c),(n-1,c)] #si le pion n'a pas été pris dans un angle : 4 posibilités
    L.remove(coord_vide)  #on ne peut pas laisser le pion où on l'a pris
    return L

def pousseok(coord_vide,case): #case = coordonnées de là où l'on veut pousser
    Lpos=poussepossible(coord_vide) #liste des positions de pousse possibles
    for k in Lpos:
        if case==k:  #si l'endroit où le joueur veut poser est dans Lposs
            return True
    return False
    

#Faire l'action 

def capture_cube(case, Plateau, joueur): #capture le cube en position case si cela est possible
    P=Plateau
    l,c=case
    positions_possibles=capture_possible(Plateau, joueur)
    if case in positions_possibles: 
        P[l,c]=vide #on enlève le cube
        return True
    return False

def pousse(coord_vide, case, Plateau_local, joueur):
    P = Plateau_local
    l,c = case #position de la case de pose
    lv,cv = coord_vide #position de la case coord_vide

    #décalage de la ligne ou de la colonne de pousse
    if l == lv:
        if c<cv:
            for k in range (cv,0,-1):
                P[l,k]=P[l,k-1]
        else : 
            for k in range (cv,n-1):
                P[l,k]=P[l,k+1]
    elif c == cv: #peut etre remplacer par else 
        if l < lv:
            for k in range (lv,0,-1):
                P[k,c]=P[k-1,c]
        else :
            for k in range (lv,n-1):
                P[k,c]=P[k+1,c]
    #le pion du joueur se retrouve à la position de pousse
    P[l,c] = joueur     

#La partie est-elle finie ?

def partie_finie(Plateau_local, joueur_local):
    P=Plateau_local
    adv=chg_joueur(joueur_local)
    V=0
    #colonnes gagnantes ?
    for c in range(n):
        colonne=[P[l,c] for l in range(n)]
        if colonne.count(adv)==n: #le joueur a fait gagné l'adversaire, il a donc perdu
            return adv
        if colonne.count(joueur_local)==n: #le joueur a une colonne gagnante
            V+=1
    #lignes gagnantes ?
    for l in range(n):
        ligne=[P[l,c] for c in range(n)]
        if ligne.count(adv)==n : #le joueur a fait gagné l'adversaire, il a donc perdu
            return adv
        if ligne.count(joueur_local)==n: #le joueur a une colonne gagnante
            V+=1
    #diagonales gagnantes ?
    diag_1=[P[k,k] for k in range (n)]
    
    if diag_1.count(adv)==n : #le joueur a fait gagné l'adversaire, il a donc perdu
        return adv
    if diag_1.count(joueur_local)==n: #le joueur a une colonne gagnante
            V+=1
            
    diag_2=[P[k,(n-1)-k] for k in range(n)]
    if diag_2.count(adv)==n : #le joueur a fait gagné l'adversaire, il a donc perdu
        return adv
    if diag_2.count(joueur_local)==n: #le joueur a une colonne gagnante
            V+=1

    if V!=0:
        return joueur_local
    else: #personne n'a gagné
        return False



##Les intelligences artificielles

#IA sans stratégie 

def IA_aleatoire(Plateau_local, joueurIA):
    coup = rd.choice(explore_1tour(Plateau_local, joueurIA)) #choisit un terme 
    return coup
    
#IA prévoyant les coups possible 

def explore_1tour(Plateau_local, joueur_local):
    all_possibilities=[]
    #choisi la case coord_vide
    for coord_vide in coord_bordure : 
        P_copie=np.copy(Plateau_local) #fonction np.copy permet une copie viable du plateau de jeu alors qu'un simple égale crée des interferences avec l'autre plateau
        if capture_cube(coord_vide, P_copie, joueur_local):
           #choisi la case de pousse
            for case in coord_bordure:
               if pousseok(coord_vide, case): 
                  P_copie2=np.copy(P_copie) #on crée un nv plateau par possibilité de pousse
                  pousse(coord_vide,case,P_copie2,joueur_local)
                  all_possibilities.append(P_copie2) #ajoute le plateau virtuel une fois le coup joué
    return all_possibilities


def poids_fenetre(fenetre, joueurIA, mode_IA): #joueurIA = celui qui joue au rg du plateau
# 1 : mode offensive 2: mode defensif
    poids= 0
    adv=chg_joueur(joueurIA)
    
    #commun quelque soit le mode de l'IA
    if fenetre.count(joueurIA) == n: #l'IA a une ligne gagnante
        poids+= 1000000           
    elif fenetre.count(adv) == n: #l'adversaire gagne
            poids -=1000000
                     
   #selon le mode de l'IA             
    if mode_IA==1:#plus l'IA aligne de pions plus la fenêtre a un poids élevé
        for k in range(n):
            if fenetre.count(joueurIA) == k :
                poids += k*10

    elif mode_IA==2: #moins l'adversaire aligne de pions plus la fenêtre a un poids élevé
        for k in range(n):
            if fenetre.count(adv) == k :
                poids += (n-k)*10
    
    return poids

def poids_plateau(Plateau_local, joueurIA, mode_IA):
    P=Plateau_local
    poids= 0
    #poids colonnes
    for c in range(n):
        colonne=[P[l,c] for l in range(n)] #la fenêtre = listes des valeurs sur la colonne c
        poids+=poids_fenetre(colonne,joueurIA, mode_IA)
    #poids lignes
    for l in range(n):
        ligne=[P[l,c] for c in range(n)]
        poids+=poids_fenetre(ligne,joueurIA, mode_IA)
    #poids diagonales
    diag_1=[P[k,k] for k in range (n)]
    poids+=poids_fenetre(diag_1,joueurIA, mode_IA)
    diag_2=[P[k,(n-1)-k] for k in range(n)]
    poids+=poids_fenetre(diag_2,joueurIA, mode_IA)

    return poids

def minimax(Plateau_local, profondeur, alpha, beta, joueur_local, modeIA):
    
    #On commence par retourner le poids du plateau dans le cas ou on est au dernier rang
    if partie_finie(Plateau_local, joueur_local)!=False or profondeur==0:
        return [None, poids_plateau(Plateau_local, joueur, modeIA)]

    #On est pas au dernier rang donc on appelle la fonction à la profondeur-1 (récursivité)    
    elif joueur_local==joueur: #on fait jouer le joueur virtuellement et on essaye de faire le meilleur coup possible
        maxi = -np.inf #moins l'infini 
        for coord_vide in capture_possible(Plateau_local, joueur_local):
            for case in poussepossible(coord_vide):
                Pcopy = np.copy(Plateau_local)
                pousse(coord_vide,case,Pcopy,joueur_local) #joue le coup
                nouveau_score = minimax(Pcopy, profondeur-1, alpha, beta, chg_joueur(joueur_local), modeIA)[1] #on prend que le poids et pas le coup
                if nouveau_score > maxi:
                    maxi = nouveau_score
                    coup = (coord_vide,case)
                alpha = max(alpha, nouveau_score) 
                if alpha >= beta: #évite de calculer des branches inutilement 
                    break
        return [coup, maxi]
    
    else: #on fait jouer l'adversaire virtuellement et on essaye de faire le pire coup possible
        mini = np.inf
        for coord_vide in capture_possible(Plateau_local, joueur_local):
            for case in poussepossible(coord_vide):
                Pcopy = np.copy(Plateau_local)
                pousse(coord_vide,case,Pcopy,joueur_local)
                nouveau_score = minimax(Pcopy, profondeur-1, alpha, beta, chg_joueur(joueur_local), modeIA)[1] #on prend que le score et pas le coup
                if nouveau_score < mini:
                    mini = nouveau_score
                    coup = (coord_vide,case)
                beta = min(beta, nouveau_score)
                if alpha >= beta:
                    break
        return [coup, mini]


##Interface graphique 


#figure
fig = plt.figure()
ax = plt.axes(aspect=1) #repère orthonormé
plt.xlim(-4,n+4) 
plt.ylim(-1,n+1)
plt.axis('off')
plt.title('QUIXO')
contour = plt.Rectangle((-1,-1),n+2,n+2,fc=(0.8,0.8,0.8)) #fc=face colour : couleur de ce qu'on trace
fond = plt.Rectangle((-4,-1),n+8,n+2,fc=(0.5,0.5,0.5))
ax.add_patch(fond)
ax.add_patch(contour)
fond_plateau = plt.Rectangle((0,0),n,n, fc=(0.4,0.25,0.2))
ax.add_patch(fond_plateau)

#boutons
bouton_newgame=plt.Rectangle((1,n+0.2),n-2,0.6,fc='black') #bouton new game
ax.add_patch(bouton_newgame)
text_newgame=plt.text(n/2,n+0.5,'New Game',fontsize=8,horizontalalignment='center',verticalalignment='center',color='w')
text_joueur1=plt.text(-2.5,n+0.5,'Consigne',fontsize=12,horizontalalignment='center',verticalalignment='center',color='black')
text_IArand=plt.text(-2.5,2*n/3,'IA aleatoire taper c',fontsize=8,horizontalalignment='center',verticalalignment='center',color='black')
text_IAoff=plt.text(-2.5,n/2,'IA offensive taper a',fontsize=8,horizontalalignment='center',verticalalignment='center',color='black')
text_IAdef=plt.text(-2.5,n/4,'IA defensive taper b',fontsize=8,horizontalalignment='center',verticalalignment='center',color='black')


#grille
for k in range (-1,n): 
    h=k+0.975
    lignev = plt.Rectangle((h,0),0.05,n,fc=(0.8,0.8,0.8))
    ligneh = plt.Rectangle((0,h),n,0.05,fc=(0.8,0.8,0.8))
    ax.add_patch(lignev)
    ax.add_patch(ligneh)


#mise à jour de la figure
def refresh(): 
    P=Plateau
    Lindetermine=[]
    Lcroix=[]
    Lrond=[]
    global coord_vide #nécessaire pour pour l'appeler dans clic
    for l in range(n):
        for c in range(n):
            case=(l,c)
            if P[l,c]==indetermine:
                Lindetermine.append(case)
    
            elif P[l,c]==croix:
                Lcroix.append(case)
            
            elif P[l,c]==rond:
                Lrond.append(case)
    
            elif P[l,c]==vide:
                coord_vide = case #pas besoin de liste, maximum une case coord_vide
                yc, xc = coord_vide 
                yc = n-1-yc #passage de la matrice a la figure
                dessinvide = plt.Rectangle((xc,yc), width=1, height=1, facecolor=(0.8,0.8,0.8)) #width=largeur et height=longueur
                ax.add_patch(dessinvide)
    
    for cube in Lcroix:
        yc, xc = cube
        yc = n-1-yc #passage de la matrice a la figure
        dessinindetermine = plt.Rectangle((xc+0.025,yc+0.025), width=0.95, height=0.95, facecolor=(0.4,0.25,0.2))
        ax.add_patch(dessinindetermine)
        branche1 = plt.Rectangle((xc+0.25,yc+0.35), width=0.1, height=0.6, angle=-45, facecolor='black') # croix= 2 rectangles avec angle 45°
        branche2 = plt.Rectangle((xc+0.65,yc+0.3), width=0.1, height=0.6, angle=45, facecolor='black')
        ax.add_patch(branche1)
        ax.add_patch(branche2)
    for cube in Lrond:
        yc, xc = cube
        yc = n-1-yc #passage de la matrice a la figure
        dessinindetermine = plt.Rectangle((xc+0.025,yc+0.025), width=0.95, height=0.95, facecolor=(0.4,0.25,0.2))
        ax.add_patch(dessinindetermine)
        dessinrond = plt.Circle((xc+0.5,yc+0.5), radius=0.3, facecolor='black')
        ax.add_patch(dessinrond)
    for cube in Lindetermine:
        yc, xc = cube
        yc = n-1-yc #passage de la matrice a la figure
        dessinindetermine = plt.Rectangle((xc+0.025,yc+0.025), width=0.95, height=0.95, facecolor=(0.4,0.25,0.2))
        ax.add_patch(dessinindetermine)


#actions declenchées par le clique de souris 

def clic(event): #pour un joueur réel 
    global joueur
    global Plateau
    x,y = event.xdata,event.ydata #récupère les coord du clique

    #Connexion du bouton "new game"
    if 1<x<n-1 and n+0.2<y<n+0.8:
        play()
        refresh()
        ax.texts=[ax.texts[k] for k in range(5)] #supprime les textes defini apres les 5 initiaux 
    
    #Au cours d'une partie
    else:
        c = int(x-x%1) #passage de la figure à la matrice
        l = int((n-1)-(y-y%1))
        case = (l,c)
        testvide = np.where(Plateau == -1, 1,0) #renvoie une matrice avec des 1 là où il y a des -1 dans le plateau et des 0 sinon
        
        #Phase de capture
        if np.any(testvide)==0: #la matrice est égale à la matrice nulle (n'importe quel élément de testvide est nul)
            print('capture')
            capture_cube(case,Plateau,joueur)
            refresh()
                      
        
        #Phase de pousse
        else: #le cube à été capturé
            if pousseok(coord_vide,case):
                pousse(coord_vide,case,Plateau,joueur)
                print('pose')
                refresh()
                
                if partie_finie(Plateau,joueur) != False: #si la partie est terminée
                    if partie_finie(Plateau,joueur)==rond:
                        gagnant="rond gagne"
                    else:
                        gagnant="croix gagne"

                    plt.text(1,-0.5,gagnant, fontsize=15, color='red')
                    
                else: #si la partie n'est pas finie
                    #changement de tour
                    joueur = chg_joueur(joueur)
                    

def clicIA(event): #pour jouer avec une IA
    global joueur
    global Plateau
    modeIA=0
    
    if event.key == 'a':
            modeIA = 1
    
    elif event.key == 'b':
            modeIA = 2
    
    if modeIA!=0:
            deb=time.time()
            ((coord_vide,case) , poids) = (minimax(Plateau, 2, -1000000000, 1000000000, joueur, modeIA)[k] for k in range(2))
            capture_cube(coord_vide, Plateau, joueur)
            refresh()
            pousse(coord_vide,case,Plateau,joueur)    
            refresh()
            fin=time.time()
            print(fin-deb)
            joueur = chg_joueur(joueur)
        
    elif event.key == 'c':
            Plateau = IA_aleatoire(Plateau, joueur)
            refresh()
            joueur = chg_joueur(joueur)

    if partie_finie(Plateau, joueur) != False:
        if partie_finie(Plateau,joueur)==rond:
            gagnant="rond gagne"
        else:
            gagnant="croix gagne"

        plt.text(1,-0.5,gagnant, fontsize=15, color='red')
    

        
fig.canvas.mpl_connect('button_press_event', clic)
fig.canvas.mpl_connect('key_press_event', clicIA)
plt.interactive(True) 
plt.pause(10000) #evite que la figure se ferme 
plt.show(block=False) #evite les bugs 


##Graphiques

#comparaison des IA 

def simulIA(IA1, IA2): #prend en entrée le mode des 2 IA dans l'ordre de jeu 
    global joueur
    global Plateau
    Plateau=np.zeros((n,n))
    joueur = 1
    modeIA = IA1
    nbcoup=0
    
    fIA1= 0
    fIA2= 0
    feg= 0
    
    for plateau in explore_1tour(Plateau,1):
        Plateau=plateau
        N=len(explore_1tour(Plateau,1))
        
        while not partie_finie(Plateau,joueur) and nbcoup<100:
            ((coord_vide,case) , poids) = (minimax(Plateau, 2, -1000000000, 1000000000, joueur, modeIA)[k] for k in range(2))
            capture_cube(coord_vide, Plateau, joueur)
            pousse(coord_vide,case,Plateau,joueur)    
            joueur = chg_joueur(joueur)
            if modeIA==IA1:
                modeIA=IA2
            else:
                modeIA=IA1
            nbcoup+=1
            
        if partie_finie(Plateau,joueur)==1:
            fIA1+=1/N
        elif partie_finie(Plateau,joueur)==2:
            fIA2+=1/N
        else:
            feg+=1/N
    
    plt.bar([1,2,3],[fIA1,fIA2,feg],width=0.5)
    handles = [plt.Rectangle((0,0),1,1,color=c,ec="k")for c in ["blue","red","grey"]]
    labels= ["IA1","IA2","égualité"]
    plt.legend(handles, labels)
    plt.show()
