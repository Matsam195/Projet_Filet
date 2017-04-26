# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 11:01:12 2017

@author: Annie
"""

from math import sqrt
import matplotlib.pyplot as plt
from Point import *

##################################################################### 
#                     FONCTION PRINCIPALE

# P1, P2, P3, P4 sont des arrays de taille 3
# l est la longueur cible
# i le nombre d'appels (pour éviter de faire une infinité d'appels...)
def optimisation(P1,P2,P3,P4, l, oldP1=0, i=0):
    assert isinstance(P1,Point) 
    assert isinstance(P2,Point) 
    assert isinstance(P3,Point) 
    assert isinstance(P4,Point) 

    # paramètres
    epsilon = 0.0001 # <----------- modifiable
    nbIteMax = 50 # <------------- modifiable
    
    # on teste qu'on n'a pas fait trop d'appels
    if i>nbIteMax:
<<<<<<< HEAD
        print("Newton : ça a pas trop l'air de converger...")
=======
        #print("ça a pas trop l'air de converger...")
>>>>>>> f05f9cb36f73090df2ccf4c95a0912a0e9f601ce
        return P1  
    
    # calcul nouveau point
    newP1=Point(P1.x, P1.y, P1.z)
    Df = DGradE(P1, P2, P3, P4, l)
    f = gradE(P1, P2, P3, P4, l)
    l1 = [Df[0][0], Df[0][1], -f[0]]
    l2 = [Df[1][0], Df[1][1], -f[1]]
    res=cramer(l1, l2)
    newP1.x = P1.x + res[0]
    newP1.y = P1.y + res[1]
    newE=gradE(newP1, P2, P3, P4, l)
<<<<<<< HEAD
        
    if (oldP1==0):
        return optimisation(newP1, P2, P3, P4, l, P1, i+1)
=======

    if (module(newE) < epsilon):
        #print("on a fait " + str(i) + " appels récursifs :)")
        return newP1
>>>>>>> f05f9cb36f73090df2ccf4c95a0912a0e9f601ce
    else:
        oldE=gradE(P1, P2, P3, P4, l)
        veryOldE=gradE(oldP1, P2, P3, P4, l)
        changement = module(diff(newE,oldE)) / module(diff(veryOldE,oldE))        
        if (changement < epsilon):
            print("on a fait " + str(i) + " appels récursifs.")
            return newP1
        else:
            return optimisation(newP1, P2, P3, P4, l, P1, i+1)

#####################################################################
#                     FONCTIONS ANNEXES

# A et B sont des list de taille 2
# on retourne A-B
def diff(A,B):
    res = [0,0]
    res[0]=A[0]-B[0]
    res[1]=A[1]-B[1]
    return res

# ---------------------------------------------------------------------
# P1, P2, P3, P4 sont des arrays de taille 3
# l est la longueur cible
def DGradE(P1,P2,P3,P4,l):
    assert isinstance(P1,Point) 
    assert isinstance(P2,Point) 
    assert isinstance(P3,Point) 
    assert isinstance(P4,Point)
    
    res = [[0.0, 0.0],[0.0, 0.0]]
    # d²E/dx²
    res[0][0]+= 3*(P1.x-P2.x)**2+(P1.y-P2.y)**2+(P1.z-P2.z)**2-l**2
    res[0][0]+= 3*(P1.x-P3.x)**2+(P1.y-P3.y)**2+(P1.z-P3.z)**2-l**2
    res[0][0]+= 3*(P1.x-P4.x)**2+(P1.y-P4.y)**2+(P1.z-P4.z)**2-l**2
    res[0][0]*= 4
    # d²E/dy²
    res[1][1]+= 3*(P1.y-P2.y)**2+(P1.x-P2.x)**2+(P1.z-P2.z)**2-l**2
    res[1][1]+= 3*(P1.y-P3.y)**2+(P1.x-P3.x)**2+(P1.z-P3.z)**2-l**2
    res[1][1]+= 3*(P1.y-P4.y)**2+(P1.x-P4.x)**2+(P1.z-P4.z)**2-l**2
    res[1][1]*= 4
    # d²E/dxdy
    res[0][1]+= (P1.x-P2.x)*(P1.y-P2.y)
    res[0][1]+= (P1.x-P3.x)*(P1.y-P3.y)
    res[0][1]+= (P1.x-P4.x)*(P1.y-P4.y)
    res[0][1]*= 8
    res[1][0]+= res[0][1]
    return res
    
# ---------------------------------------------------------------------
# P1, P2, P3, P4 sont des arrays de taille 3
# l est la longueur cible  
def gradE(P1,P2,P3,P4,l):
    assert isinstance(P1,Point) 
    assert isinstance(P2,Point) 
    assert isinstance(P3,Point) 
    assert isinstance(P4,Point)
    
    res = [0.0,0.0]    
    # dE/dx
    res[0]+= (P1.x-P2.x)*((P1.x-P2.x)**2+(P1.y-P2.y)**2+(P1.z-P2.z)**2-l**2)
    res[0]+= (P1.x-P3.x)*((P1.x-P3.x)**2+(P1.y-P3.y)**2+(P1.z-P3.z)**2-l**2)
    res[0]+= (P1.x-P4.x)*((P1.x-P4.x)**2+(P1.y-P4.y)**2+(P1.z-P4.z)**2-l**2)
    res[0]*= 4
    # dE/dy
    res[1]+= (P1.y-P2.y)*((P1.x-P2.x)**2+(P1.y-P2.y)**2+(P1.z-P2.z)**2-l**2)
    res[1]+= (P1.y-P3.y)*((P1.x-P3.x)**2+(P1.y-P3.y)**2+(P1.z-P3.z)**2-l**2)
    res[1]+= (P1.y-P4.y)*((P1.x-P4.x)**2+(P1.y-P4.y)**2+(P1.z-P4.z)**2-l**2)
    res[1]*= 4
    return res

# ---------------------------------------------------------------------
# le système est : e1[0]*x + e1[1]*y = e1[2] 
#                  e2[0]*x + e2[1]*y = e2[2]
def cramer(e1,e2):
    res = [0.0,0.0] 
    determinant=e1[0]*e2[1]-e1[1]*e2[0]
    assert(determinant!=0)
    res[0]=(e1[2]*e2[1]-e1[1]*e2[2])/determinant
    res[1]=(e1[0]*e2[2]-e1[2]*e2[0])/determinant
    return res
    
# ---------------------------------------------------------------------  
def module(E):
    return sqrt(E[0]**2+E[1]**2)
    
#####################################################################
#                     EXEMPLES D'UTILISATION
    
# ---------------------------------------------------------------------   
# Exemple simple
# attendu : P1opt = (1/sqrt2, 1/sqrt2)
# bleus: voisins
# rouge: point initial
# jaune: point optimisé
    
#P1=Point(1.0/sqrt(2.0)+0.3, 1.0/sqrt(2.0)+0.1, 0.0)
#P2=Point(0.0, 0.0, 0.0)
#P3=Point(2.0/sqrt(2.0), 0.0, 0.0)
#P4=Point(1.0/sqrt(2.0), 1.0+1.0/sqrt(2.0), 0.0)
#newP1=optimisation(P1,P2,P3,P4,1, 0)
#plt.plot([P2.x, P3.x, P4.x], [P2.y, P3.y, P4.y], 'bo')
#plt.plot([P1.x], [P1.y], 'ro')
#plt.plot([newP1.x], [newP1.y], 'yo')
#plt.show()
#print("Point optimise attendu : (", 1/sqrt(2), ";", 1/sqrt(2), ")")
#print("Point optimise trouve : (", newP1.x, ";", newP1.y, ")")
#plt.figure()

# ---------------------------------------------------------------------
# Exemple moins simple
# attendu : P1opt = (1/sqrt2, un peu + que 1/sqrt2)
# bleus: voisins
# rouge: point initial
# jaune: point optimisé

#P1=Point(1.0/sqrt(2.0)+0.3, 1.0/sqrt(2.0)+0.1, 0.0)
#P2=Point(0.0, 0.0, 0.0)
#P3=Point(2.0/sqrt(2.0), 0.0, 0.0)
#P4=Point(1.0/sqrt(2.0), 1.2+1.0/sqrt(2.0), 0.0)
#newP1=optimisation(P1,P2,P3,P4,1,0)
#plt.plot([P1.x, P2.x, P3.x, P4.x], [P1.y, P2.y, P3.y, P4.y], 'go')
#plt.plot([newP1.x], [newP1.y], 'yo')
#plt.show()
#print("Point optimise attendu : (", 1/sqrt(2), ";", 1/sqrt(2), " + epsilon)")
#print("Point optimise trouve : (", newP1.x, ";", newP1.y, ")")