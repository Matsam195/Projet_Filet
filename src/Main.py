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
maille = Maille(15,5)
# Création de l'origine - 1er papillon en (0,0)
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

ponderations = [1,0.6,0]

for k in range(1, N+1):
    t = k/N
    St = interpolation(S0, SN, t)
    mailleCour.projection(St)
    stable = False
    nbOpti = 0
    while (not estStable(mailleCour, L, angle, ponderations) and nbOpti < 25):
        nbOpti += 1
        #print("########################### N'est pas stable. Optimisation", nbOpti, "de l'interpolation", k, "... #############################")
        for i in range(1, mailleCour.n-1):
            for j in range(1, mailleCour.m-1):
#                print("Point de coordonnées ", i, j)
                v = mailleCour.getVoisins(i,j)
                p = mailleCour.get(i,j)
                mailleSuiv.pts[i + j*(mailleCour.n)] = optimisation(p, v[0], v[1], v[2], L, angle, ponderations)
        mailleCour = mailleSuiv
    print("Tour numero " + str(k) + " fini")
#    mailleCour.afficher()

mailleCour.afficher()

