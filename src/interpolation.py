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
    amplitude = 3
    sigma = 1 # Ecart-type
    mu = [4, 3] # Centrer la Gaussienne
    return Point(u,v, amplitude/(sigma*sqrt(2*pi)) * exp(-((u-mu[0])**2 + (v-mu[1])**2)/(sigma*sigma*2)))
    
    
