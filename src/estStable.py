# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 16:05:12 2017

@author: belotm
"""

from Maille import *
from Papillon import *
from Point import *

# Condition de stabilité
c = 0.2 #<---- à modifier

# Longueur des barres rigides
l = 1

def assezProche(point, voisin):
<<<<<<< HEAD
    return point.distance(voisin)-l<=c
=======
    return point.distance(voisin)-l<=0.2
>>>>>>> f05f9cb36f73090df2ccf4c95a0912a0e9f601ce

def estStable(M2Dtemp):
    for i in range(1, M2Dtemp.n-1):
        for j in range(1, M2Dtemp.m-1):
            for v in M2Dtemp.getVoisins(i, j):
                if (not assezProche(M2Dtemp.get(i,j), v)):
                    return False
    return True