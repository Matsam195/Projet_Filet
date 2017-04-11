# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 16:05:12 2017

@author: belotm
"""

from Maille import *
from Papillon import *
from Point import *

# Longueur des barres rigides
l = 3

def assezProche(point, voisin, epsilon):
    return distance(point, voisin)-longueur<=epsilon

def estStable(M2Dtemp):
    for point in M2Dtemp:
        for voisin in listeVoisins(point):
            if (not assezProche(point, voisin, epsilon)):
                return False
    return True