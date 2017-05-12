# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 16:05:12 2017

@author: belotm
"""

from Maille import *
from Papillon import *
from Point import *

# Condition de stabilité
c = 0.01 #<---- à modifier

# Longueur des barres rigides
l = 0.5

def assezProche(point, voisin):
    return abs(point.distance(voisin)-l)<=c

def estStable(M2Dtemp):
    for i in range(1, M2Dtemp.n-1):
        for j in range(1, M2Dtemp.m-1):
            for v in M2Dtemp.getVoisins(i, j):
                if (not assezProche(M2Dtemp.get(i,j), v)):
                    return False
    return True