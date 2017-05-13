# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from math import *
import matplotlib.pyplot as plt

class Point:
    """Classe définissant un point selon ses coordonnées (x,y,z)"""

    def __init__(self, x=0, y=0, z=0):
        """Création d'un point selon ses trois coordonnées (x,y,z)"""
        self.x = x
        self.y = y
        self.z = z

    def distance(self, point):
        """Calcul de la distance entre deux points"""
        return sqrt((self.x - point.x)**2
                    + (self.y - point.y)**2
                    + (self.z - point.z)**2)

    def afficherPoint(self) :
        """Affichage du point"""
        if not(self.x == -1 and self.y == -1):
            plt.plot(self.x, self.y, 'ro')

    def afficherSegment(self, p2) :
        """Affichage du segment entre le point en paramètre et l'objet"""
        plt.plot( [self.x, p2.x], [self.y, p2.y] )