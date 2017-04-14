# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 15:01:04 2017

@author: batim
"""

import numpy as np
from Point import *
from Papillon import *


class Maille:
    """Une maille comporte la taille n*m et une grille de papillons"""
        
    def __init__(self, a, b):
        self.n = a # n papillons pour la hauteur de la grille
        self.m = b # m papillons pour la largeur de la grille
        self.pap = []
        
    #Les positions i (resp j) vont de la valeur 0 à n exclue (resp m)
    def placerPapillon(self, papillon):
        self.pap.append(papillon)
            
    def afficher(self):
        print("taille : ")
        print(self.n)
        print(self.m)
        
    def get(self, i, j):
        assert((i >= 0) and (i < self.n) and (j >= 0) and (j < self.m))
        return self.pap[i + j*(self.n)] # *(self.m-1)
        
    def modifierPapillon(self, i, j, papillon):
        if (i >= 0) and (i < self.n) and (j >= 0) and (j < self.m):
            self.pap[i + j*(self.n-1)] = papillon 