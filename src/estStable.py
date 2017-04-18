# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 16:05:12 2017

@author: belotm
"""

from Maille import *
from Papillon import *
from Point import *

# Longueur des barres rigides
l = 1

def assezProche(point, voisin):
    return point.distance(voisin)-l<=0.1

def estStable(M2Dtemp):
    for i in range(1, M2Dtemp.n-1):
        for j in range(1, M2Dtemp.m-1):
            for v in M2Dtemp.getVoisins(i, j):
                if (not assezProche(M2Dtemp.get(i,j), v)):
                    return False
    return True