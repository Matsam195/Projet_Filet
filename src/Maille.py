# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 15:01:04 2017

@author: batim
"""

import numpy as np
from Point import *
from Papillon import *
#from Papillon import *


class Maille:
    """Une maille comporte la taille n*m et une grille de papillons"""
 #   def __init__(self):
  #      self.n = 0
   #     self.m = 0
    #    for i in range(self.n):
     #       for j in range(self.m):
      #          self.pap[i][j] = Papillon(Point(), 0, 0, 0)
        
    def __init__(self, a, b):
        self.n = a
        self.m = b
        self.pap = [self.n, self.m]
        #[self.n][self.m]
        #for i in range(self.n):
        #    for j in range(self.m):
        #        self.pap[i][j] = Papillon(Point(0,0,0), 0, 0, 0)
        #self.pap = np.zeros((a,b))
        
    #Les positions i (resp j) vont de la valeur 0 à n exclue (resp m)
    def placerPapillon(self, i, j, papillon):
        if (i >= 0) and (i < self.n) and (j >= 0) and (j < self.m):
            self.pap[i, j] = papillon