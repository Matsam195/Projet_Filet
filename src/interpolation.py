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
    return Point(u,v, 17*v)
    

print(interpolation(S0, SN, 1)(1,2).x)
print(interpolation(S0, SN, 1)(1,2).y)
print(interpolation(S0, SN, 1)(1,2).z)