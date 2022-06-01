""""PROGRAMMATION DU JEU QUIXO"""
"""Pour jouer, lancer le programme en appuyant sur "Ctrl E" 
règle du jeu : sélectionnez un pion sur la périphérie du plateau puis reposez le de sorte que le vide soit comblé en cliquant sur un des cubes d'une extrémité opposée
But du jeu : aligner n de ses symboles (n : dimension du plateau)
Jouer avec les IA : Pour faire jouer une IA appuyer sur la touche du clavier indiquée sur le bord gauche du plateau"""

"""Pour tracer un graphique (comparaison des IA, efficacité du programme), appeller la fontion correspondante (voir fin de programme)"""

##Importations
import numpy as np
import matplotlib.pyplot as plt
import random as rd
import time

##Définition des variables globales

#correspondance objet/matrice
croix=1
rond=2
indetermine=0
vide=-1

#mode IA
OFFENSIF=1
DEFENSIF=2

def chg_joueur(joueur_local):
    """renvoie l'adversaire du joueur entré en argument"""
    if joueur_local==croix:
        joueur_local=rond
    else:
        joueur_local=croix
    return joueur_local

#choix de la taille du plateau
n=5

##Mise en place du jeu

def play():
    """initialisation du plateau de jeu et choix du joueur qui commence"""
    global Plateau
    Plateau=np.zeros((n,n))
    global joueur
    joueur = rd.randint(croix,rond) #le joueur 1 ou le joueur 2 commence (hasard)
play()

def set_coord_bordure():
    """renvoie la liste des coordonées matricielles de la bordure du plateau"""
    L1=[(0,k) for k in range(n)]
    L2=[(n-1,k) for k in range(n)]
    L3=[(k,0) for k in range(1,n-1)]
    L4=[(k,n-1) for k in range(1,n-1)]
    L=L1+L2+L3+L4
    return L

coord_bordure=set_coord_bordure()

#Peut-on effectuer l'action ?

def capture_possible(Plateau_local, joueur_local):
    """Prend en argument un plateau et un joueur et renvoie la liste des coordonnées des cubes que le joueur peut capturer"""
    L=[]
    for coord in set_coord_bordure():
        if Plateau_local[coord]==joueur_local or Plateau_local[coord]==indetermine:
            L.append(coord)
    return L

def poussepossible(coord_vide):
    """Prend en argument les coordonnées de la case vide et renvoie la liste des coordonnées où la pousse est possible"""
    l,c = coord_vide
    A=[(0,0),(0,n-1),(n-1,0),(n-1,n-1)] #coordonnées des angles
    if coord_vide in A: #si le pion a été pris dans un angle : 2 possiblités
      return [(abs(l-(n-1)),c),(l,abs((n-1)-c))] #on fixe l ou c
    L=[(l,0),(l,n-1),(0,c),(n-1,c)] #si le pion n'a pas été pris dans un angle : 4 posibilités
    L.remove(coord_vide)  #on ne peut pas laisser le pion où on l'a pris
    return L

def pousseok(coord_vide,case):
    """Prend en arguments les coordonnées de la case vide et de la case où l'on veut pousser et renvoit un booléen"""
    return (case in poussepossible(coord_vide)) #liste des positions de pousse possibles


#Faire l'action

def capture_cube(Plateau_local, joueur, case):
    """Prend en argument un plateau, un joueur et les coordonnées de la case où le joueur veut capture puis capture"""
    P=Plateau_local
    l,c=case
    if case in capture_possible(P, joueur):
        P[l,c]=vide #on enlève le cube

def pousse(Plateau_local, joueur, coord_vide, case):
    """Prend en argument un plateau, un joueur, les coordonnées de la case où il souhaite pousser et celles de la case vide puis pousse """
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
    elif c == cv: #peut être remplacé par else
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
    """Prend en argument plateau et joueur : renvoie le gagnant si la partie est finie, False sinon"""
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
    """Joue au hasard"""
    c=rd.choice(capture_possible(Plateau_local, joueurIA))
    p=rd.choice(poussepossible(c))
    P=np.copy(Plateau_local)
    capture_cube(P, joueurIA, c)
    pousse(P, joueurIA, c, p)
    return P


#IA prévoyant les coups possible

def poids_fenetre(fenetre, joueurIA, mode_IA):
    """"Pour un alignement de n cases (=fenêtre) renvoie un entier (=poids) d'autant plus grand que la fenêtre est avantageuse pour le joueur"""
    poids= 0
    adv=chg_joueur(joueurIA)

    #commun quelque soit le mode de l'IA
    if fenetre.count(joueurIA) == n: #l'IA a une ligne gagnante
        poids+= 1000000
    elif fenetre.count(adv) == n: #l'adversaire gagne
            poids -=1000000

   #selon le mode de l'IA
    if mode_IA==OFFENSIF:#plus l'IA aligne de pions plus la fenêtre a un poids élevé
        for k in range(n):
            if fenetre.count(joueurIA) == k :
                poids += k*10

    elif mode_IA==DEFENSIF: #moins l'adversaire aligne de pions plus la fenêtre a un poids élevé
        for k in range(n):
            if fenetre.count(adv) == k :
                poids += (n-k)*10

    return poids

def poids_plateau(Plateau_local, joueurIA, mode_IA):
    """Retourne le poids du plateau par rapport au joueur et à sa stratégie de jeu (mode_IA) """
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

def minimax(Plateau_local, joueur_local, profondeur, modeIA, alpha, beta):
    """Parcours de manière récursive l'arbre des possibilités de jeu jusqu'à une profondeur donnée et retourne le coup le plus avantageux pour le joueur et son poids"""

    #On commence par retourner le poids du plateau dans le cas ou on est au dernier rang
    if partie_finie(Plateau_local, joueur_local)!=False or profondeur==0:
        return [None, poids_plateau(Plateau_local, joueur, modeIA)]

    #On est pas au dernier rang donc on appelle la fonction à la profondeur-1 (récursivité)
    elif joueur_local==joueur: #on fait jouer le joueur virtuellement
        maxi = -np.inf #moins l'infini
        for coord_vide in capture_possible(Plateau_local, joueur_local):
            for case in poussepossible(coord_vide):
                Pcopy = np.copy(Plateau_local)
                pousse(Pcopy,joueur_local,coord_vide,case) #joue le coup
                nouveau_score = minimax(Pcopy, chg_joueur(joueur_local), profondeur-1, modeIA, alpha, beta)[1] #on prend que le poids et pas le coup
                if nouveau_score > maxi:
                    maxi = nouveau_score
                    coup = (coord_vide,case)
                alpha = max(alpha, nouveau_score)
                if alpha >= beta: #évite de calculer des branches inutilement
                    break
        return [coup, maxi]

    else: #on prédit le coup de l'adversaire virtuellement
        mini = np.inf
        for coord_vide in capture_possible(Plateau_local, joueur_local):
            for case in poussepossible(coord_vide):
                Pcopy = np.copy(Plateau_local)
                pousse(Pcopy,joueur_local,coord_vide,case)
                nouveau_score = minimax(Pcopy, chg_joueur(joueur_local), profondeur-1,modeIA, alpha, beta)[1] #on prend que le score et pas le coup
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
text_consignes=plt.text(-2.5,n+0.5,'Consignes',fontsize=12,horizontalalignment='center',verticalalignment='center',color='black')
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
    """Actualise l'interface graphique à partir de la matrice plateau"""
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

def clic(event):
    """Déclenche une série d'action à partir du clique du joueur sur l'interface graphique"""
    global joueur
    global Plateau
    x,y = event.xdata,event.ydata #récupère les coord du clique

    #Connexion du bouton "new game"
    if 1<x<n-1 and n+0.2<y<n+0.8:
        play()
        refresh()
        ax.texts=[ax.texts[k] for k in range(5)] #supprime tous les textes sauf ceux nécessaires au début de partie

    #Au cours d'une partie
    else:
        c = int(x-x%1) #passage de la figure à la matrice (x%1: reste de la division euclidienne par 1 <=> chiffre après la virgule)
        l = int((n-1)-(y-y%1))
        case = (l,c)
        testvide = np.where(Plateau == -1, 1,0) #renvoie une matrice avec des 1 là où il y a des -1 dans le plateau et des 0 sinon

        #Phase de capture
        if np.any(testvide)==0: #la matrice est égale à la matrice nulle (n'importe quel élément de testvide est nul)
            capture_cube(Plateau,joueur,case)
            refresh()


        #Phase de pousse
        else: #le cube à été capturé
            if pousseok(coord_vide,case):
                pousse(Plateau,joueur,coord_vide,case)
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
    """Déclenche le jeu d'une IA selon la touche du clavier pressée"""
    global joueur
    global Plateau
    modeIA=0

    if event.key == 'a':
            modeIA = 1

    elif event.key == 'b':
            modeIA = 2
            
    if modeIA!=0:
            deb=time.time()
            ((coord_vide,case) , poids) = (minimax(Plateau, joueur, 2, modeIA, -1000000000, 1000000000)[k] for k in range(2))
            capture_cube(Plateau, joueur, coord_vide)
            refresh()
            pousse(Plateau,joueur,coord_vide,case)
            refresh()
            fin=time.time()
            #print(fin-deb)
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
plt.pause(10000) #évite que la figure se ferme
plt.show(block=False) #évite les bugs


##Graphiques

#comparaison des IA

def simulIA(IA1, IA2):#Pour que la fonction trace le graphique il faut commenter toute la partie interface graphique 
    """Prend en entrée le mode de 2 IA et affiche les fréquences de victoires de chacune"""
    global joueur
    global Plateau
    Plateau=np.zeros((n,n))
    joueur = 1
    modeIA = IA1
    nbcoup=0
    nbparties=0
    
    fIA1= 0
    fIA2= 0
    feg= 0
    
    for c in capture_possible(Plateau, 1): #on test tous les 1er coups possibles différents
        for p in poussepossible(c) :
            capture_cube(Plateau, 1, c)
            pousse(Plateau, 1, c, p)
            nbparties+=1
            while not partie_finie(Plateau,joueur) and nbcoup<100:
                ((coord_vide,case) , poids) = (minimax(Plateau, joueur, 2, modeIA, -1000000000, 1000000000)[k] for k in range(2))
                capture_cube(Plateau, joueur,coord_vide)
                pousse(Plateau,joueur,coord_vide,case)
                joueur = chg_joueur(joueur)
                if modeIA==IA1:
                    modeIA=IA2
                else:
                    modeIA=IA1
                nbcoup+=1

            if partie_finie(Plateau,joueur)==1:
                fIA1+=1/nbparties
            elif partie_finie(Plateau,joueur)==2:
                fIA2+=1/nbparties
            else:
                feg+=1/nbparties

    plt.bar([1,2,3],[fIA1,fIA2,feg],width=0.5)
    handles = [plt.Rectangle((0,0),1,1,color=c,ec="k")for c in ["blue","red","grey"]]
    labels= ["IA1","IA2","égualité"]
    plt.legend(handles, labels)
    plt.show()
    

#Efficacité du programme 

#valeur recupérer grâce à la bibliothèque time
L_prof_1_elagage=[0.032422542572021484,0.03390192985534668,0.03288841247558594,0.03688979148864746,0.05303382873535156,0.0339496135711669,0.03333449363708496,0.03889942169189453,0.03737473487854004,0.0460817813873291,0.04139208793640137,0.04031872749328613,0.048400163650512695,0.04485344886779785,0.044895172119140625,0.04483342170715332,0.0362548828125,0.03539419174194336,0.03601336479187012]
L_prof_2_elagage=[0.28851318359375,0.2601969242095947,0.26482439041137695,0.23706388473510742,0.2294912338256836,0.24045634269714355,0.18215036392211914,0.19139742851257324,0.19612741470336914,0.2076098918914795,0.16843128204345703,0.1560497283935547,0.14779973030090332,0.14177989959716797,0.13069987297058105,0.15012860298156738,0.15142321586608887,0.13753700256347656,0.14173460006713867,0.11642265319824219]
L_prof_3_elagage=[4.85296893119812,4.385595798492432,4.158659219741821,3.8172338008880615,3.2782204151153564,3.555518388748169,2.515331506729126,2.6929337978363037,2.744154214859009,2.8351833820343018,2.6712000370025635,2.2165017127990723,2.2029197216033936,1.86653733253479,1.7297430038452148,1.4150440692901611,2.2472991943359375,1.822556495666504,1.2208962440490723,1.453660488128662,1.433415174484253]
L_prof_4_elagage=[89.4329879283905,65.89046096801758,74.624803543090,2,48.774333238601685,69.9312047958374,57.91015696525574,68.44473218917847,59.9443724155426,35.98308539390564]

L_prof_1=[0.0338895320892334,0.03176569938659668,0.03393316268920898,0.03188896179199219,0.03394317626953125,0.035935163497924805,0.036879539489746094,0.037865638732910156,0.03888702392578125,0.03493475914001465,0.04086613655090332,0.03887176513671875,0.03780937194824219,0.04485273361206055,0.08192563056945801,0.0440521240234375,0.0524907112121582,0.02990126609802246,0.032410383224487305,0.03588128089904785]
L_prof_2=[0.6372017860412598,0.6384100914001465,0.566535234451294,0.5361955165863037,0.5006463527679443,0.4783594608306885,0.45131993293762207,0.497161865234375,0.409984827041626,0.39862847328186035,0.35509681701660156,0.3452920913696289,0.29601120948791504,0.28644800186157227,0.25717949867248535,0.25258612632751465,0.24218153953552246,0.2101128101348877,0.21529197692871094,0.19671344757080078]
L_prof_3=[27.981194257736206,24.32934021949768,23.035787343978882,20.623336791992188,19.019317626953125,24.742548942565918,17.288718938827515,18.402055263519287,13.838642358779907,16.1404550075531,12.491037130355835,10.200233697891235,10.849183559417725,8.412062406539917,7.692501068115234,6.447391986846924,6.476495027542114,6.221293926239014,5.428781747817993,5.432814359664917]
L_prof_4=[200] #bcp plus de 200s en réalité, l'ordinateur n'achève pas le calcul 

def temps_prof_avec_sans_elagage():
    """Comparaison du temps de calcul avec ou sans élagage , selon la profondeur entrée en argument de minimax()"""
    X=np.linspace(1,4,4)
    Y1=[np.mean(L_prof_1_elagage),np.mean(L_prof_2_elagage),np.mean(L_prof_3_elagage),np.mean(L_prof_4_elagage)]
    Y2=[np.mean(L_prof_1),np.mean(L_prof_2),np.mean(L_prof_3),np.mean(L_prof_4)]
    plt.plot(X,Y1, label="t=f(profondeur) avec elagage")
    plt.plot(X,Y2, label="t=f(profondeur) sans elagage")
    plt.xlabel("profondeur de calcul")
    plt.ylabel("temps que met l'IA pour jouer (s)")
    plt.legend()
    plt.show()

