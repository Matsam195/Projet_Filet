# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 12:01:39 2017

@author: batim
"""

from math import *
from Point import *
from Papillon import *
from Maille import *
from ListePoints import *
from interpolation import *
from estStable import *
from optimisation import *



L = 0.5
angle = pi/2.5
# On génère un nombre fixe de papillons 
maille = Maille(24,10)
# Création de l'origine - 1er papillon en (0,0)
# Garder 0,0,0 est une bonne idée car il existe des "points fantomes" aux bords
# qui risquent de poser problème si la maille est centrée en 0
origine = Point(0, 0, 0)






premierPapillon = Papillon(origine, L, L, angle)
maille.placerPapillon(premierPapillon)
#premierPapillon.tracer()
courant = premierPapillon
# Création de la première colonne :
i = 0
while i != maille.n -1:
    if (i%2) == 0:
        suivant = courant.ajouterPapillonInitColonne(courant.nm, courant.ne, pi/2.5)
    else :
        suivant = courant.ajouterPapillonInitColonne(courant.no, courant.nm, pi/2.5)
    maille.placerPapillon(suivant)
#    suivant.tracer()
    courant = suivant    
    i = i + 1
    
# Création des autres papillons 
j = 1 # on a déjà tracé la première colonne donc on commence à 1
while (j < maille.m):
    # Papillon "du bas" - sur le bord
    courant = maille.get(0, j-1).ajouterPapillonHrzt(maille.get(1, j-1).se)
#    courant.tracer()
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
#        suivant.tracer()
        maille.placerPapillon(suivant)
        courant = suivant      
        i = i + 1
    j = j + 1
    
#plt.axis([0, 8, 0, 4])
#plt.show() 

liste_pts = ListePoints(maille)
#liste_pts.afficher()
#plt.show()


######################################################################################################################

mailleCour = liste_pts
mailleSuiv = liste_pts
# S0 fonction définie dans interpolation
# SN fonction définie dans interpolation

N = 10
x = []
y = []

ponderations = [1,0,0]
E = L - 2*L*cos(angle)

for k in range(1, N+1):
    t = k/N
    St = interpolation(S0, S0, t)
    mailleCour.projection(St)
    stable = False
    nbOpti = 0
    while (not estStable(mailleCour, L, E, angle, ponderations) and nbOpti < 10):
        nbOpti += 1
        #print("########################### N'est pas stable. Optimisation", nbOpti, "de l'interpolation", k, "... #############################")
        
        #Optimisation des bords
        for i in [0, mailleCour.n-1]:
            for j in range(0, mailleCour.m):
                v = mailleCour.getVoisins(i,j)
                p = mailleCour.get(i,j)
                print(i + j*(mailleCour.n))
                mailleSuiv.pts[i + j*(mailleCour.n)] = optimisation(p, v[0], v[1], v[2], v[3], L, E, angle, ponderations)
        for j in [0, mailleCour.m-1]:
            for i in range(0, mailleCour.n):  
                v = mailleCour.getVoisins(i,j)
                p = mailleCour.get(i,j)
                mailleSuiv.pts[i + j*(mailleCour.n)] = optimisation(p, v[0], v[1], v[2], v[3], L, E, angle, ponderations)

        #Optimisation des autres points
        for i in range(1, mailleCour.n-1):
            for j in range(1, mailleCour.m-1):
#                print("Point de coordonnées ", i, j)
                v = mailleCour.getVoisins(i,j)
                p = mailleCour.get(i,j)
                mailleSuiv.pts[i + j*(mailleCour.n)] = optimisation(p, v[0], v[1], v[2], v[3], L, E, angle, ponderations)
        mailleCour = mailleSuiv
    print("Tour numero " + str(k) + " fini")
#    mailleCour.afficher()

mailleCour.afficher()

