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


def capture_cube(case): #capture le cube en position case si cela est possible
    P=Plateau
    l,c=case
    positions_possibles=[]# récupère les coordonnées (i,j) de tout les endroits ou le joueur peut jouer un nouveau coup , en bordure!
    for position in coord_bordure:#lp=ligne du doublet dans position cp=colonne du doublet dans position
        lp,cp=position
        if P[lp,cp]==0 or P[lp,cp]==joueur:
             positions_possibles.append((lp,cp))
    if case in positions_possibles: #verifie que  la position est valide
        P[l,c]=-1 #on enlève le cube, -1=case vide
        print(P)
        return True
    return False

##Peut-on pousser ici ?
def poussepossible(case): #renvoie liste des coorconnées des posi° où on peut pousser
    l,c = case
    A=[(0,0),(0,4),(4,0),(4,4)] #listes des coord des angles
    if case in A: #si le pion a été pris dans un angle
      return [(abs(l-4),c),(l,abs(4-c))]#on fixe l ou c , on determine les endroits ou on peut pousser par la relation avec abs() (faire dessin)
    L=[(l,0),(l,4),(0,c),(4,c)] #si le pion n'a pas été pris dans un angle 4 posibilités
    for k in range(4):
        if L[k]==case:
            del L[k]     #on ne peut pas laisser le pion où on l'a pris
        return L

def pousseok(vide,case): #case = coordonnées de là où on veut pousser
    Lpos=poussepossible(vide) #liste des positions de pousse possibles
    for k in Lpos:
        if case==k:  #l'endroit où le joueur veut poser est dans Lposs => c ok
            return True
    return False

## Pousse de la ligne ou de la colonne
def pousse(vide,case):
    P = Plateau
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
    print(P)

##fonction partie finie
def check(list): 
   return list.count(list[0]) == len(list) #on compte le nombre d'occurence du premier element , si il est egal à la taille de la liste alors la liste est formée d'elements identiques

def partie_finie():
    P=Plateau
    coord_ligne_haut=[(0,k) for k in range (5)]
    coord_colonne_gauche=[(k,0) for k in range (5)]
    coord_diag_1=[(k,k) for k in range (5)]
    coord_diag_2=[(4,0),(3,1),(2,2),(1,3),(0,4)]
    for coord in coord_ligne_haut: #une colonne gagnante? #pourquoi ne pas remplacer par un simple compteur?
        bin,c=coord
        colonne=[P[k,c] for k in range(5)] #on recupère les données de chaque colonne 
        if check(colonne) and colonne[0]!=0: #la fonction check() renvoie True si les elements d'une liste sont identiques
            return [True,colonne[0]]
    for coord in coord_colonne_gauche: #une ligne gagnante? #pourquoi ne pas remplacer par un simple compteur?
        l,bin=coord
        ligne=[P[l,k] for k in range(5)]
        if check(ligne) and ligne[0]!=0:
            return [True,ligne[0]]
    diag_1=[P[coord] for coord in coord_diag_1]
    diag_2=[P[coord] for coord in coord_diag_1]
    if check(diag_1) and diag_1[0]!=0 : #la premiere diagonale gagnante?
        return [True,diag_1[0]]
    elif check(diag_2) and diag_2[0]!=0: #la 2ème diagonale gagnante?
        return [True,diag_2[0]]
    return [False]

    


#------------------------------------------------------Interface Graphique-----------------------------------------------------------

##figure 
#xc,yc correspont au sommet bas gauche de chaque case dans le graphique
fig = plt.figure()
ax = plt.axes(aspect=1) #repère orthonormé
plt.xlim(-1,6) 
plt.ylim(-1,6)
plt.axis('off')
plt.title('QUIXO')
contour = plt.Rectangle((-1,-1),7,7,fc=(0.8,0.8,0.8)) #fc=face colour : couleur de ce qu'on trace
ax.add_patch(contour)
fond = plt.Rectangle((0,0),5,5, fc=(0.4,0.25,0.2))
ax.add_patch(fond)
bouton=plt.Rectangle((1,5.2),3,0.6,fc='black') #bouton new game
ax.add_patch(bouton)
newgame=plt.text(2.5,5.5,'New Game',fontsize=10,horizontalalignment='center',verticalalignment='center',color='w')
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
    x,y = event.xdata,event.ydata #récupère les coord du clique
    
    #Connexion du bouton "new game"
    if 1<x<4 and 5.2<y<5.8:
        play()
        refresh()
        ax.texts=[ax.texts[0]] #supprime tous les textes sauf "newgame" defini en premier
    
    #Au cours d'une partie
    else:
        c = int(x-x%1) #passage de la figure à la matrice
        l = int(4-(y-y%1))
        case = (l,c)
        testvide = np.where(Plateau == -1)[0]
        
        if testvide.size == 0: #vérifie que aucun cube n'a deja été sélectioné
            print('capture')
            capture_cube(case)
            refresh()
        
        else: #le cube à été capturé, phase de pousse.
            print('test pose')
            if pousseok(vide, case):
                pousse(vide,case)
                print('pose')
                refresh()
                
                if partie_finie()[0]:
                    gagnant=partie_finie()[1]
                    if gagnant==1:
                        gagnant="croix gagne"
                    else:
                        gagnant="rond gagne"
                    plt.text(1.5,-0.5,gagnant, fontsize=15, color='red')
                
                else: #si la partie n'est pas finie
                    #changement de tour
                    global joueur
                    if joueur==1:
                        joueur=2
                    else:
                        joueur=1
    


fig.canvas.mpl_connect('button_press_event', clic)
plt.interactive(True) 
plt.pause(10000) #evite que la figure se ferme 
plt.show(block=False) #evite les bugs 


     

    
