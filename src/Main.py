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


### Paramètres de la simulation ###
L = 0.5
angle = pi/2.5
N = 10
dz = valeurdz(SN, N)
bordsLibres = False
ponderations = [1,0,1]
E = L - 2*L*cos(angle)
nbOptiMax = 1000
###

liste_pts = ListePoints(17, 8, L, angle)
mailleCour = liste_pts
mailleSuiv = liste_pts
x = []
y = []

for k in range(1, N+1):
    t = k/N
    St = interpolation(S0, SN, t)
    mailleCour.projection(St)
    nbOpti = 0
    while (not estStable2(mailleCour, L, E, angle, ponderations, dz=dz) and nbOpti < nbOptiMax):
        nbOpti += 1
        #Optimisation des bords
        if (bordsLibres):
            for i in [0, mailleCour.n-1]:
                for j in range(0, mailleCour.m):
                    v = mailleCour.getVoisins(i,j)
                    p = mailleCour.get(i,j)
                    if (p.x != -1):
                        mailleSuiv.pts[i*mailleCour.m + j] = optimisation(p, v[0], v[1], v[2], v[3], ponderations, L, E, angle, dz=dz)
            for j in [0, mailleCour.m-1]:
                for i in range(0, mailleCour.n):  
                    v = mailleCour.getVoisins(i,j)
                    p = mailleCour.get(i,j)
                    if p.x != -1:
                        mailleSuiv.pts[i*mailleCour.m + j] = optimisation(p, v[0], v[1], v[2], v[3], ponderations, L, E, angle, dz=dz)
                
        #optimisation des points intérieurs
        for i in range(1, mailleCour.n-1):
            for j in range(1, mailleCour.m-1):
                v = mailleCour.getVoisins(i,j)
                p = mailleCour.get(i,j)
                #mailleSuiv.pts[i*mailleCour.m + j] = optimisation(p, v[0], v[1], v[2], v[3], ponderations, L, E, angle, dz=dz)
        mailleCour = mailleSuiv
    if (nbOpti == nbOptiMax):
        print("Nombre d'optimisation maximal atteint. Passage à l'interpolation suivante.")
    print("Interpolation", str(k), "finie au bout de", nbOpti, "optimisations")
#    mailleCour.afficher()

mailleCour.afficher()
