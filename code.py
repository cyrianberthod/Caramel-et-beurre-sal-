##Importations
import numpy as np
import matplotlib as plt
#on pose l=ligne et c=colonne

#------------------------------------------------Matrice-------------------------------------------------------------------------------
##initialiation
def plateau():
  P=np.zeros(5,5)
  return P



## Pousse de la ligne ou de la colonne
def pousse(clic):
    if not poussepossible(clic):
        print("pose impossible") #à modifier comme vous voulez
    else:
        l,c=clic #position de la case de pose
        lv,cv=vide #position de la case vide
        if poussepossible(clic):
            #décalage de la ligne ou de la colonne de pousse
            if l==lv:
                if c<cv:
                    for k in range (cv,0,-1):
                        P[l,k]=P[l,k-1]
                elif c>cv: #peut etre remplacer par else si impossible de poser au même endroit
                    for k in range (cv,5):
                        P[l,k]=P[l,k+1]
            elif c==cv: #peut etre remplacer par else 
                if l<lv:
                    for k in range (lv,0,-1):
                        P[k,c]=P[k-1,c]
                elif c>cv: #peut etre remplacer par else si impossible de poser au même endroit
                    for k in range (lv,5):
                        P[k,c]=P[k+1,c]
            #pose du cube à la position de pousse           
            P[l,c]=joueur 

#------------------------------------------------------Interface Graphique-----------------------------------------------------------
