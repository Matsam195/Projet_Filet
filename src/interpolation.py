# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 16:13:43 2017

@author: mariono
"""
from Point import *

def interpolation(S0, SN, t):        
    return (lambda u,v:Point(S0(u,v).x*(1-t) + t*SN(u,v).x, S0(u,v).y*(1-t) + t*SN(u,v).y,  S0(u,v).z*(1-t) + t*SN(u,v).z))
    
def S0(u,v):
    return Point(u,v, 0)
    
def SN(u,v):
    amplitude = 6
    sigma = 2 # Ecart-type
    mu = [5, 5] # Centrer la Gaussienne
    return Point(u,v, amplitude/(sigma*sqrt(2*pi)) * exp(-((u-mu[0])**2 + (v-mu[1])**2)/(sigma*sigma*2)))
    
    
