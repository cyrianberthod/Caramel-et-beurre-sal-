##Importations
import numpy as np
import matplotlib as plt
#on pose l=ligne et c=colonne

#------------------------------------------------Matrice-------------------------------------------------------------------------------
##initialiation
def plateau():
  P=np.zeros((5,5))
  return P

def capture_cube(joueur,clic):
    P=plateau()
    l,c=clic
    positions_possibles=[]# récupère les coordonnées (i,j) de tout les endroits ou le joueur peut jouer un nouveau coup , en bordure!
    for position in coord_bordure:#lp=ligne du doublet dans position cp=colonne du doublet dans position
        lp,cp=position
        if P[lp,cp]==0 or P([lp,cp])==joueur:
             positions_possibles.append((l,c))
    if (l,c) in positions_possibles: #verifie que  la position est la valide
        P[l,c]=-1 #on enlève le cube, -1=case vide
        print(P)
        return (True,(l,c))
    return False

##Peut-on pousser ici ?
def poussepossible(l,c): #renvoie liste des coorconnées des posi° où on peut pousser
    A=[(0,0),(0,4),(4,0),(4,4)] #listes des coord des angles
    if (l,c) in A: #si le pion a été pris dans un angle
      return [(abs(l-4),c),(l,abs(4-c))]#on fixe l ou c , on determine les endroits ou on peut pousser par la relation avec abs() (faire dessin)
    L=[(l,0),(l,4),(0,c),(4,c)] #si le pion n'a pas été pris dans un angle 4 posibilité
    for k in range(4):
        if L[k]==(l,c):
            del L[k]     #on ne peut pas laisser le pion où on l'a pris
            return L

def pousseok(l,c,pl,pc): #(pl,pc) coordonnées de là où on veut pousser
    Lpos=poussepossible(l,c) #liste des positions de pousse possibles
    for k in Lpos:
        if (pl,pc)==k:  #l'endroit où le joueur veut poser est dans Lposs => c ok
            return True
    return False

## Pousse de la ligne ou de la colonne
def pousse(clic):
    if not pousseok(clic):
        print("pose impossible") #à modifier comme vous voulez
    else:
        l,c=clic #position de la case de pose
        lv,cv=vide #position de la case vide

        #décalage de la ligne ou de la colonne de pousse
        if l==lv:
            if c<cv:
                for k in range (cv,0,-1):
                    P[l,k]=P[l,k-1]
            elif c>cv: #peut etre remplacer par else si impossible de poser au même endroit
                for k in range (cv,4):
                    P[l,k]=P[l,k+1]
        elif c==cv: #peut etre remplacer par else 
            if l<lv:
                for k in range (lv,0,-1):
                    P[k,c]=P[k-1,c]
            elif l>lv: #peut etre remplacer par else si impossible de poser au même endroit
                for k in range (lv,4):
                    P[k,c]=P[k+1,c]
            
        #pose du cube à la position de pousse           
        P[l,c]=joueur 
 

#------------------------------------------------------Interface Graphique-----------------------------------------------------------

fig = plt.figure()
ax = plt.axes(aspect=1)
plt.xlim(-0.1,0.6)
plt.ylim(-0.1,0.6)
plt.axis('off')
plt.title('QUIXO')
contour = plt.Rectangle((-0.1,-0.1),0.7,0.7,fc=(0.8,0.8,0.8))
ax.add_patch(contour)
fond = plt.Rectangle((0,0),0.5,0.5, fc=(0.4,0.25,0.2))
ax.add_patch(fond)
for k in range (0,4): #grille
    h=k/10+0.0975
    lignev = plt.Rectangle((h,0),0.005,0.5,fc="black")
    ligneh = plt.Rectangle((0,h),0.5,0.005,fc="black")
    ax.add_patch(lignev)
    ax.add_patch(ligneh)

plt.show()
