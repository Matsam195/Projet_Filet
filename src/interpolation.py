# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 16:13:43 2017

@author: mariono
"""
from Point import *

def interpolation(S0, SN, t):
    """
    Fonction lambda qui calcule l'interpolation au temps t entre 0 et 1
    """
    return (lambda u,v:Point(S0(u,v).x*(1-t) + t*SN(u,v).x, S0(u,v).y*(1-t) + t*SN(u,v).y,  S0(u,v).z*(1-t) + t*SN(u,v).z))
    
def S0(u,v):
    """
    Surface plane
    """
    return Point(u,v, 0)
    
def SN(u,v):
    """
    Surface 
    """
    amplitude = 2
    sigma = 1 # Ecart-type
    mu = [3.5, 3.5] # Centrer la Gaussienne
    return Point(u,v, amplitude/(sigma*sqrt(2*pi)) * exp(-((u-mu[0])**2 + (v-mu[1])**2)/(sigma*sigma*2)))
    
# def S_lat(u,v):
#     return Point(u,v, cos(v))

def valeurdz(SN, N):
    """
    Renvoie le dz max entre 2 surfaces subissant une interpolation de N surfaces
    """ 
    maxX=10.0 #domaine dans le x entre 0 et maxX
    maxY=10.0 #domaine dans le y entre 0 et maxY
    k = 100 #nb d'interpolation de la grille de recherche
    max = 0.0
    for i in range(1,k):
        for j in range(1,k):
            res=SN(float(i)*maxX/float(k),float(j)*maxY/float(k)).z
            if (res > max):
                max = res
    return (float(max)/float(N))