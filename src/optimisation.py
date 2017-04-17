# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 11:01:12 2017

@author: Annie
"""

from math import sqrt
import matplotlib.pyplot as plt

##################################################################### 
# P1, P2, P3, P4 sont des arrays de taille 3
# l est la longueur cible
# i le nombre d'appels (pour éviter de faire une infinité d'appels...)
def optimisation(P1, P2, P3, P4, l, i):
    
    # paramètres
    epsilon = 0.0001 # <----------- modifiable
    nbIteMax = 100 # <------------- modifiable
    
    # on teste qu'on n'a pas fait trop d'appels
    if i>nbIteMax:
        print("ça a pas trop l'air de converger...")
        return P1
        
    # calcul nouveau point
    newP1=[P1[0],P1[1],P1[2]]
    Df = DGradE(P1, P2, P3, P4, l)
    f = gradE(P1, P2, P3, P4, l)
    l1 = [Df[0][0], Df[0][1], -f[0]]
    l2 = [Df[1][0], Df[1][1], -f[1]]
    res=cramer(l1, l2)
    newP1[0]=P1[0]+res[0]
    newP1[1]=P1[1]+res[1]
    newE=gradE(newP1, P2, P3, P4, l)

    if (module(newE) < epsilon):
        print("on a fait " + str(i) + " appels récursifs :)")
        return newP1
    else:
        return optimisation(newP1, P2, P3, P4, l, i+1)

#####################################################################   
# P1, P2, P3, P4 sont des arrays de taille 3
# l est la longueur cible
def DGradE(P1,P2,P3,P4,l):
    res = [[0.0, 0.0],[0.0, 0.0]]
    # d²E/dx²
    res[0][0]+= 3*(P1[0]-P2[0])**2+(P1[1]-P2[1])**2+(P1[2]-P2[2])**2-l**2
    res[0][0]+= 3*(P1[0]-P3[0])**2+(P1[1]-P3[1])**2+(P1[2]-P3[2])**2-l**2
    res[0][0]+= 3*(P1[0]-P4[0])**2+(P1[1]-P4[1])**2+(P1[2]-P4[2])**2-l**2
    res[0][0]*= 4
    # d²E/dy²
    res[1][1]+= 3*(P1[1]-P2[1])**2+(P1[0]-P2[0])**2+(P1[2]-P2[2])**2-l**2
    res[1][1]+= 3*(P1[1]-P3[1])**2+(P1[0]-P3[0])**2+(P1[2]-P3[2])**2-l**2
    res[1][1]+= 3*(P1[1]-P4[1])**2+(P1[0]-P4[0])**2+(P1[2]-P4[2])**2-l**2
    res[1][1]*= 4
    # d²E/dxdy
    res[0][1]+= (P1[0]-P2[0])*(P1[1]-P2[1])
    res[0][1]+= (P1[0]-P3[0])*(P1[1]-P3[1])
    res[0][1]+= (P1[0]-P4[0])*(P1[1]-P4[1])
    res[0][1]*= 8
    res[1][0]+= res[0][1]
    return res

#####################################################################
# P1, P2, P3, P4 sont des arrays de taille 3
# l est la longueur cible  
def gradE(P1,P2,P3,P4,l):
    res = [0.0,0.0]    
    # dE/dx
    res[0]+= (P1[0]-P2[0])*((P1[0]-P2[0])**2+(P1[1]-P2[1])**2+(P1[2]-P2[2])**2-l**2)
    res[0]+= (P1[0]-P3[0])*((P1[0]-P3[0])**2+(P1[1]-P3[1])**2+(P1[2]-P3[2])**2-l**2)
    res[0]+= (P1[0]-P4[0])*((P1[0]-P4[0])**2+(P1[1]-P4[1])**2+(P1[2]-P4[2])**2-l**2)
    res[0]*= 4
    # dE/dy
    res[1]+= (P1[1]-P2[1])*((P1[0]-P2[0])**2+(P1[1]-P2[1])**2+(P1[2]-P2[2])**2-l**2)
    res[1]+= (P1[1]-P3[1])*((P1[0]-P3[0])**2+(P1[1]-P3[1])**2+(P1[2]-P3[2])**2-l**2)
    res[1]+= (P1[1]-P4[1])*((P1[0]-P4[0])**2+(P1[1]-P4[1])**2+(P1[2]-P4[2])**2-l**2)
    res[1]*= 4
    return res

#####################################################################
# le système est : e1[0]*x + e1[1]*y = e1[2] 
#                  e2[0]*x + e2[1]*y = e2[2]
def cramer(e1,e2):
    res = [0.0,0.0] 
    determinant=e1[0]*e2[1]-e1[1]*e2[0]
    if determinant==0:
        print('Pas de solution unique')
    else:
        res[0]=(e1[2]*e2[1]-e1[1]*e2[2])/determinant
        res[1]=(e1[0]*e2[2]-e1[2]*e2[0])/determinant
    return res
    
def module(E):
    return sqrt(E[0]**2+E[1]**2)
    
#####################################################################
# Exemple simple
# attendu : P1opt = (1/sqrt2, 1/sqrt2)
# bleus: voisins
# rouge: point initial
# jaune: point optimisé
P1=[1.0/sqrt(2.0)+0.3, 1.0/sqrt(2.0)+0.1, 0.0]
P2=[0.0, 0.0, 0.0]
P3=[2.0/sqrt(2.0), 0.0, 0.0]
P4=[1.0/sqrt(2.0), 1.0+1.0/sqrt(2.0), 0.0]
newP1=optimisation(P1,P2,P3,P4,1, 0)
plt.plot([P2[0], P3[0], P4[0]], [P2[1], P3[1], P4[1]], 'bo')
plt.plot([P1[0]], [P1[1]], 'ro')
plt.plot([newP1[0]], [newP1[1]], 'yo')

#####################################################################
# Exemple moins simple
# attendu : P1opt = (1/sqrt2, un peu + que 1/sqrt2)
# bleus: voisins
# rouge: point initial
# jaune: point optimisé
P1=[1.0/sqrt(2.0)+0.3, 1.0/sqrt(2.0)+0.1, 0.0]
P2=[0.0, 0.0, 0.0]
P3=[2.0/sqrt(2.0), 0.0, 0.0]
P4=[1.0/sqrt(2.0), 1.2+1.0/sqrt(2.0), 0.0]
#newP1=optimisation(P1,P2,P3,P4,1,0)
#plt.plot([P1[0], P2[0], P3[0], P4[0]], [P1[1], P2[1], P3[1], P4[1]], 'bo')
#plt.plot([newP1[0]], [newP1[1]], 'yo')