# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 16:05:12 2017

@author: belotm
"""

from Maille import *
from Papillon import *
from Point import *
from optimisation import *

# Condition de stabilité
seuil = 0.01 #<---- à modifier

def energieAssezFaible(point, voisins, longueur, angle):
    return(Energie(point, voisins[0], voisins[1], voisins[2], longueur, angle) < seuil)

def estStable(maille, longueur, angle):
    for i in range(1, maille.n-1):
        for j in range(1, maille.m-1):
            point = maille.get(i,j)
            voisins = maille.getVoisins(i, j)
            if (not energieAssezFaible(point, voisins, longueur, angle)):
                return False
    return True