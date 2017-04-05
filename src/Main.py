# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 12:01:39 2017

@author: batim
"""

from math import *
from Point import *
from Papillon import *
from Maille import *

angle = pi/2.5
# On génère un nombre fixe de papillons 
maille = Maille(4,5)

# Création de l'origine - 1er papillon en (0,0)
origine = Point(0, 0, 0)
premierPapillon = Papillon(origine, 1, 1, angle)
maille.placerPapillon(premierPapillon)
premierPapillon.tracer()
courant = premierPapillon 
# Création de la première colonne :
i = 0
while i != maille.n -1:
    if (i%2) == 0:
        suivant = courant.ajouterPapillonInitColonne(courant.nm, courant.ne, pi/2.5)
    else :
        suivant = courant.ajouterPapillonInitColonne(courant.no, courant.nm, pi/2.5)
    maille.placerPapillon(suivant)
    suivant.tracer()
    courant = suivant    
    i = i + 1
    
# Création des autres papillons 
j = 1 # on a déjà tracé la première colonne donc on commence à 1
while (j < maille.m):
    # Papillon "du bas" - sur le bord
    courant = maille.get(0, j-1).ajouterPapillonHrzt(maille.get(1, j-1).se)
    courant.tracer()
    maille.placerPapillon(courant)
    i = 1
    # Papillons à l'intérieur
    while (i < maille.n):
        if (i%2) != 0:
            suivant = courant.ajouterPapillonVertSimple(maille.get(i, j-1)) 
        else:
            if i == maille.n - 1:
                suivant = courant.ajouterPapillonVertDernier(maille.get(i, j-1))
            else:
                suivant = courant.ajouterPapillonVert(maille.get(i, j-1), maille.get(i+1,j-1).se)
        suivant.tracer()
        maille.placerPapillon(suivant)
        courant = suivant      
        i = i + 1
    j = j + 1
    
plt.axis([0, 8, 0, 4])
plt.show() 


# transformation des mailles de papillons en liste de points

####### Entrées : 
N = 10 			# Nb itérations
SN = ? 			# surface à approcher

####### Variables :
# A définir à partir de l’initialisation déjà faite :
M2Dfinal = 		# Maille temporaire 2D, paramétrisation u v


for t in range(1/N,1/N,1):  
    # interpolation de la surface pour trouver la nouvelle : S = (1-t) S0 + t SN
    Scour = interpolation(S0, SN, t) 	# surface idéale interpolée au temps t
    stable = False 			          # critère d’arrêt sur les longueurs calculées
    M2Dtemp = M2Dfinal          		# maillage 2D temporaire
    
    # projection 3D la maille 2D des papillons, on veut que ça colle le plus possible avec Scour
    M3Dtemp = fonction(M2Dfinal, Scour);
    
    while !stable: 
        for each point2D de M2Dtemp:
            for each voisin de point2D: 
                # calcul la longueur 3D entre le point et son voisin
                dist = distance3D(M3Dtemp(point2D), voisin)
                # mémorisation des longueurs cibles 2D pour l’opti
                tab[voisin] =  longueurActuelle2D(point3D, voisin) * l / dist
                
            # optimisation locale des forces pour savoir où placer le point2D  
            # résultat dans une nouvelle maille
            M2Dtemp(point2D) = optimisation(point2D, voisins, tab) // renvoie un point2D
        
        # on regarde si toutes les longueurs sont cohérentes, 
        # sinon il faut recommencer à partir de ce résultat
        for point2D in M2Dtemp:
            for point2D in voisins:
                stable &= assezProche(point2D, voisin)
                # il faudra break dès qu’on a un false
    M2Dfinal = M2Dtemp 


####### Sortie : 
tracer(M3Dtemp) 	# on peut aussi afficher le maillage 2D : M2Dfinal




# liste de points :  
# en hauteur : nb pap + 1
# sur le côté : nb pap*2 + 2

# on trace les deux premières colonnes :
#while i < n:
#    liste.append(maille(i,0).so)
#    liste.append(maille(i,0).no)
#    i = i + 2
#    
#while i < n:
#    liste.append(maille(i,0).sm)
#    liste.append(maille(i,0).nm)
#    i = i + 2
    
# on trace le corps, à chaque coup on a deux colonnes créées :
#j = 2
#while j < n:
#    while i < n: