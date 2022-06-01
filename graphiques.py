import numpy as np
import matplotlib.pyplot as mp
L_prof_1_elagage=[0.032422542572021484,0.03390192985534668,0.03288841247558594,0.03688979148864746,0.05303382873535156,0.0339496135711669,0.03333449363708496,0.03889942169189453,0.03737473487854004,0.0460817813873291,0.04139208793640137,0.04031872749328613,0.048400163650512695,0.04485344886779785,0.044895172119140625,0.04483342170715332,0.0362548828125,0.03539419174194336,0.03601336479187012]
#print(np.mean(L_prof_1_elagage))

L_prof_2_elagage=[0.28851318359375,0.2601969242095947,0.26482439041137695,0.23706388473510742,0.2294912338256836,0.24045634269714355,0.18215036392211914,0.19139742851257324,0.19612741470336914,0.2076098918914795,0.16843128204345703,0.1560497283935547,0.14779973030090332,0.14177989959716797,0.13069987297058105,0.15012860298156738,0.15142321586608887,0.13753700256347656,0.14173460006713867,0.11642265319824219]
#np.mean(L_prof_2_elagage)
L_prof_3_elagage=[4.85296893119812,4.385595798492432,4.158659219741821,3.8172338008880615,3.2782204151153564,3.555518388748169,2.515331506729126,2.6929337978363037,2.744154214859009,2.8351833820343018,2.6712000370025635,2.2165017127990723,2.2029197216033936,1.86653733253479,1.7297430038452148,1.4150440692901611,2.2472991943359375,1.822556495666504,1.2208962440490723,1.453660488128662,1.433415174484253]
#np.mean(L_prof_3_elagage)
L_prof_4_elagage=[89.4329879283905,65.89046096801758,74.624803543090,2,48.774333238601685,69.9312047958374,57.91015696525574,68.44473218917847,59.9443724155426,35.98308539390564]
#np.mean(L_prof_4_elagage)

def affichage_temps_fonction_prof_elagage():
    X=np.linspace(1,4,4)
    Y=[np.mean(L_prof_1_elagage),np.mean(L_prof_2_elagage),np.mean(L_prof_3_elagage),np.mean(L_prof_4_elagage)]
    mp.plot(X,Y)
    mp.show()
   
 #affichage_temps_fonction_prof_elagage
L_prof_1=[0.0338895320892334,0.03176569938659668,0.03393316268920898,0.03188896179199219,0.03394317626953125,0.035935163497924805,0.036879539489746094,0.037865638732910156,0.03888702392578125,0.03493475914001465,0.04086613655090332,0.03887176513671875,0.03780937194824219,0.04485273361206055,0.08192563056945801,0.0440521240234375,0.0524907112121582,0.02990126609802246,0.032410383224487305,0.03588128089904785]

L_prof_2=[0.6372017860412598,0.6384100914001465,0.566535234451294,0.5361955165863037,0.5006463527679443,0.4783594608306885,0.45131993293762207,0.497161865234375,0.409984827041626,0.39862847328186035,0.35509681701660156,0.3452920913696289,0.29601120948791504,0.28644800186157227,0.25717949867248535,0.25258612632751465,0.24218153953552246,0.2101128101348877,0.21529197692871094,0.19671344757080078]

L_prof_3=[27.981194257736206,24.32934021949768,23.035787343978882,20.623336791992188,19.019317626953125,24.742548942565918,17.288718938827515,18.402055263519287,13.838642358779907,16.1404550075531,12.491037130355835,10.200233697891235,10.849183559417725,8.412062406539917,7.692501068115234,6.447391986846924,6.476495027542114,6.221293926239014,5.428781747817993,5.432814359664917]

L_prof_4=[200]
def affichage_temps_sans_elagage_fonction_prof():
    X=np.linspace(1,4,4)
    Y=[np.mean(L_prof_1),np.mean(L_prof_2),np.mean(L_prof_3),np.mean(L_prof_4)]
    mp.plot(X,Y)
    mp.show()

#affichage_temps_sans_elagage_fonction_prof()
def affichage_tout():
    X=np.linspace(1,4,4)
    Y1=[np.mean(L_prof_1_elagage),np.mean(L_prof_2_elagage),np.mean(L_prof_3_elagage),np.mean(L_prof_4_elagage)]
    Y2=[np.mean(L_prof_1),np.mean(L_prof_2),np.mean(L_prof_3),np.mean(L_prof_4)]
    mp.plot(X,Y1,label="t=f(prof) avec elagage")
    mp.plot(X,Y2,label="t=f(prof) sans elagage")
    mp.legend()
    mp.show()

#affichage_tout()


## en fonction de la dimension (à copier coller sous minimax)

def temps_calcul2():
    global n 
    global coord_bordure
    global joueur
    global Plateau
    modeIA=1
    profondeur=3
    T=[]
    for dim in range(3,20):
        n=dim
        Plateau=np.zeros((n,n))
        debut=time.time()
        ((coord_vide,case) , poids) = (minimax(Plateau, profondeur, -1000000000, 1000000000, joueur, modeIA)[k] for k in range(2))
        capture_cube(coord_vide, Plateau, joueur)
        pousse(coord_vide,case,Plateau,joueur)   
        fin=time.time() 
        T.append(fin-debut)
    X=[k for k in range(3,20)]
    plt.scatter(X, T, marker="+")
    plt.xlabel("dimension du plateau")
    plt.ylabel("temps que met l'IA pour jouer (s)")
    plt.show()

    
  def simulalea(IA, joueur_commencant): #joueur_commancant : 1 pour IA def/of 2 pour IA aléatoire
    """Prend en entrée une IA offensive ou défensive et si elle joue en 1er ou en 2eme : fait jouer cette IA contre l'IA aléatoire et affiche les fréquences de victoires de chacune"""
    global joueur
    global Plateau
    Plateau=np.zeros((n,n))
    joueur = joueur_commencant
    modeIA = IA
    nbcoup=0
    nbparties=0

    fIA= 0
    falea= 0
    feg= 0

    for c in capture_possible(Plateau, 1): #on test tous les 1er coups possibles différents
        for p in poussepossible(c) :
            capture_cube(Plateau, 1, c)
            pousse(Plateau, 1, c, p)
            nbparties+=1
            while not partie_finie(Plateau,joueur) and nbcoup<100:
                if joueur==1:
                    ((coord_vide,case) , poids) = (minimax(Plateau, joueur, 2, modeIA, -1000000000, 1000000000)[k] for k in range(2))
                    capture_cube(Plateau, joueur,coord_vide)
                    pousse(Plateau,joueur,coord_vide,case)
                    joueur = chg_joueur(joueur)
                else:
                    Plateau =IA_aleatoire(Plateau,joueur)
                nbcoup+=1

            if partie_finie(Plateau,joueur)==1:
                fIA+=1
            elif partie_finie(Plateau,joueur)==2:
                falea+=1
            else:
                feg+=1

    plt.bar([1,2,3],[fIA,falea,feg],width=0.5)
    handles = [plt.Rectangle((0,0),1,1,color=c,ec="k")for c in ["blue","red","grey"]]
    labels= ["IA","aléatoire","égalité"]
    plt.legend(handles, labels)
    plt.show()

