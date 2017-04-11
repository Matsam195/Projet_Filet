# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from math import *
import matplotlib.pyplot as plt

class Point:
    """Classe définissant d'un point en 3D, qui est libre ou non"""

    def __init__(self):
        """Par défaut le point3D est placé à l'origine"""
        self.x = 0
        self.y = 0
        self.z = 0
        self.libre = True
        
        
    def __init__(self, x, y):
        """Création d'un point2D"""
        self.x = x
        self.y = y
        self.z = 0
        self.libre = True
        
    def __init__(self, x, y, z):
        """Création d'un point3D"""
        self.x = x
        self.y = y
        self.z = z
        self.libre = True
        
    def distance(self, point):
        """Calcul de la distance entre deux points"""
        return sqrt((self.x - point.x)**2 
                    + (self.y - point.y)**2 
                    + (self.z - point.z)**2)  
                    

    
    def afficherPoint(self) : 
        print(self.x, self.y)
        if not(self.x == -1 and self.y == -1):
            plt.plot(self.x, self.y, 'ro')
        
    def afficherSegment(self, p2) : 
        plt.plot( [self.x, p2.x], [self.y, p2.y] )
    
