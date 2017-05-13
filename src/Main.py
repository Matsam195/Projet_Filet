# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 12:01:39 2017

@author: batim
"""

from math import *
from Point import *
from ListePoints import *
from interpolation import *
from estStable import *
from optimisation import *



L = 0.5
angle = pi/2.5
origine = Point(0, 0, 0)
liste_pts = ListePoints(25, 15, L, angle, origine)
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
    St = interpolation(S0, SN, t)
    mailleCour.projection(St)
    stable = False
    nbOpti = 0
    while (not estStable2(mailleCour, L, E, angle, ponderations) and nbOpti < 50):
        nbOpti += 1
        #print("########################### N'est pas stable. Optimisation", nbOpti, "de l'interpolation", k, "... #############################")
        for i in range(1, mailleCour.n-1):
            for j in range(1, mailleCour.m-1):
#                print("Point de coordonnées ", i, j)
                v = mailleCour.getVoisins(i,j)
                p = mailleCour.get(i,j)
                mailleSuiv.pts[i*mailleCour.m + j] = optimisation(p, v[0], v[1], v[2], v[3], ponderations, L, E, angle)
        mailleCour = mailleSuiv
    print("Tour numero " + str(k) + " fini")
#    mailleCour.afficher()

mailleCour.afficher()
