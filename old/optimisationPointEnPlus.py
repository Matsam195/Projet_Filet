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
def optimisation(P1,P2,P3,P4,P5, l, oldP1=0, i=0):
    """
    Calcule la position optimale du point P1 par rapport à ses points
    voisins P2, P3, P4, lorsque la distance désirée entre ces points vaut l.
    P1, P2, P3, P4 : objets de type Point
    l : distance désirée entre les points
    oldP1 : Ne rien mettre, sert à l'appel récursif
    i : Ne rien mettre, sert à compter le nombre d'appels récursifs effectués
    Résultat : un Point qui est la nouvelle position optimisée de P1
    """
    assert isinstance(P1,Point) 
    assert isinstance(P2,Point) 
    assert isinstance(P3,Point) 
    assert isinstance(P4,Point) 
    assert isinstance(P5,Point) 

    # paramètres
    epsilon = 0.01 # Marge d'écart autorisée pour considérer optimisation finie
    nbIteMax = 50 # Nombre d'itérations maximales autorisées
    
    # on teste qu'on n'a pas fait trop d'appels
    if i>nbIteMax:
        #print("Newton : ça a pas trop l'air de converger...")
        return P1
    
    # calcul nouveau point
    #print("Energie à l'itération ", i, " : ", Energie(P1, P2, P3, P4, l))
    #print("Point à l'itération ", i, " : ", P1.x, P1.y)
    newP1=Point(P1.x, P1.y, P1.z) # X(k+1) dans la méthode de Newton
    Df = DGradE(P1, P2, P3, P4, P5, l) # Jacobien du Gradient de E
    f = gradE(P1, P2, P3, P4, P5, l) # Gradient de E
    l1 = [Df[0][0], Df[0][1], -f[0]] # Ligne 1 Système de Cramer (ligne 120)
    l2 = [Df[1][0], Df[1][1], -f[1]] # Ligne 2
    res=cramer(l1, l2) # Résolution du système de Cramer
    newP1.x = P1.x + res[0] # X(k+1) = Z + X(k) dans les notes d'Annie
    newP1.y = P1.y + res[1]
    if (oldP1==0): # Au moins un tour d'optimisation
        return optimisation(newP1, P2, P3, P4, P5, l, P1, i+1)
    else:
        oldE=f
        veryOldE=gradE(oldP1, P2, P3, P4, P5, l)
        if (module(diff(veryOldE,oldE))==0):
            return newP1
        changement = abs(P1.distance(newP1) - oldP1.distance(P1))      
        if (changement < epsilon):
            #print("on a fait " + str(i) + " appels récursifs.")
            #print("Fini ! Energie finale : ", Energie(newP1, P2, P3, P4, l))
            return newP1
        else:
            return optimisation(newP1, P2, P3, P4, P5, l, P1, i+1)

#####################################################################
#                     FONCTIONS ANNEXES

def diff(A,B):
    """
    Retourne la différence A-B
    A et B sont des vecteurs de dimension 2
    """
    res = [0,0]
    res[0]=A[0]-B[0]
    res[1]=A[1]-B[1]
    return res

def Energie(P1,P2,P3,P4,P5,l,e):
    """
    Renvoie l'énergie d'un point P1 par rapport à ses voisins P2, P3, P4,
    pour une longueur cible l.
    P1, P2, P3, P4 : objets de type Point
    l : distance désirée entre les points
    e : distance idéale avec le voisin "non relié"
    Résultat : la valeur de l'énergie
    """
    return((P1.distance(P2)**2 - l**2)**2 + (P1.distance(P3)**2 - l**2)**2 + 
        (P1.distance(P4)**2 - l**2)**2 + (P1.distance(P5)**2 -e**2))

def DGradE(P1,P2,P3,P4,P5,l,e):
    """
    Renvoie le jacobien du gradient de E pour le point P1 et ses vosisins
    P1, P2, P3, P4 avec pour longueur cible l.
    P1, P2, P3, P4 : objets de type Point
    l : distance désirée entre les points
    e : distance idéale au voisin "non relié"
    Résultat : une matrice 2*2
    """
    assert isinstance(P1,Point) 
    assert isinstance(P2,Point) 
    assert isinstance(P3,Point) 
    assert isinstance(P4,Point)
    assert isinstance(P5,Point)

    d = P1.distance(P5) - e**2    
    
    res = [[0.0, 0.0],[0.0, 0.0]]
    # d²E/dx²
    res[0][0]+= 3*(P1.x-P2.x)**2+(P1.y-P2.y)**2+(P1.z-P2.z)**2-l**2
    res[0][0]+= 3*(P1.x-P3.x)**2+(P1.y-P3.y)**2+(P1.z-P3.z)**2-l**2
    res[0][0]+= 3*(P1.x-P4.x)**2+(P1.y-P4.y)**2+(P1.z-P4.z)**2-l**2
    res[0][0]+= 2*(P1.x - P5.x)**2 + d 
    res[0][0]*= 4 
    # d²E/dy²
    res[1][1]+= 3*(P1.y-P2.y)**2+(P1.x-P2.x)**2+(P1.z-P2.z)**2-l**2
    res[1][1]+= 3*(P1.y-P3.y)**2+(P1.x-P3.x)**2+(P1.z-P3.z)**2-l**2
    res[1][1]+= 3*(P1.y-P4.y)**2+(P1.x-P4.x)**2+(P1.z-P4.z)**2-l**2
    res[0][0]+= 2*(P1.y - P5.y)**2 + d
    res[1][1]*= 4 
    # d²E/dxdy
    res[0][1]+= (P1.x-P2.x)*(P1.y-P2.y)
    res[0][1]+= (P1.x-P3.x)*(P1.y-P3.y)
    res[0][1]+= (P1.x-P4.x)*(P1.y-P4.y)
    res[0][1]+= (P1.x-P5.x)*(P1.y-P5.y)
    res[0][1]*= 8
    res[1][0]+= res[0][1]
    return res
    
def gradE(P1,P2,P3,P4,l,e):
    """
    Renvoie le gradient de E pour le point P1 et ses vosisins
    P1, P2, P3, P4 avec pour longueur cible l.
    P1, P2, P3, P4 : objets de type Point
    l : distance désirée entre les points
    e : distance idéale au voisin "non relié"
    Résultat : un vecteur de dimension 2
    """
    assert isinstance(P1,Point) 
    assert isinstance(P2,Point) 
    assert isinstance(P3,Point) 
    assert isinstance(P4,Point)
    
    d = P1.distance(P5) - e**2  
    
    res = [0.0,0.0]    
    # dE/dx
    res[0]+= (P1.x-P2.x)*((P1.x-P2.x)**2+(P1.y-P2.y)**2+(P1.z-P2.z)**2-l**2)
    res[0]+= (P1.x-P3.x)*((P1.x-P3.x)**2+(P1.y-P3.y)**2+(P1.z-P3.z)**2-l**2)
    res[0]+= (P1.x-P4.x)*((P1.x-P4.x)**2+(P1.y-P4.y)**2+(P1.z-P4.z)**2-l**2)
    res[0]+= (P1.x-P5.x)*d
    res[0]*= 4
    # dE/dy
    res[1]+= (P1.y-P2.y)*((P1.x-P2.x)**2+(P1.y-P2.y)**2+(P1.z-P2.z)**2-l**2)
    res[1]+= (P1.y-P3.y)*((P1.x-P3.x)**2+(P1.y-P3.y)**2+(P1.z-P3.z)**2-l**2)
    res[1]+= (P1.y-P4.y)*((P1.x-P4.x)**2+(P1.y-P4.y)**2+(P1.z-P4.z)**2-l**2)
    res[1]+= (P1.y-P5.y)*d
    res[1]*= 4
    return res

def cramer(e1,e2):
    """
    Renvoie la solution (x,y) du système de Cramer
    e1[0]*x + e1[1]*y = e1[2]
    e2[0]*x + e2[1]*y = e2[2]
    e1, e2 : vecteurs de dimension 3 définissant le système
    Résultat : un vecteur de dimension 2 solution du système
    """
    res = [0.0,0.0]
    determinant=e1[0]*e2[1]-e1[1]*e2[0]
    assert(determinant!=0)
    res[0]=(e1[2]*e2[1]-e1[1]*e2[2])/determinant
    res[1]=(e1[0]*e2[2]-e1[2]*e2[0])/determinant
    return res
     
def module(E):
    """
    Renvoie le module du vecteur E de dimension 2
    """
    return sqrt(E[0]**2+E[1]**2)
    
#####################################################################
#                     EXEMPLES D'UTILISATION
    
# ---------------------------------------------------------------------   
# Exemple simple
# attendu : P1opt = (1/sqrt2, 1/sqrt2)
# bleus: voisins
# rouge: point initial
# jaune: point optimisé
    
#P1=Point(1.0/sqrt(2.0)+0.3, 1.0/sqrt(2.0)+0.3, 0.0)
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
#plt.plot([P1.x], [P1.y], 'ro')
#plt.plot([newP1.x], [newP1.y], 'yo')
#plt.show()
#print("Point optimise attendu : (", 1/sqrt(2), ";", 1/sqrt(2), " + epsilon)")
#print("Point optimise trouve : (", newP1.x, ";", newP1.y, ")")



# ---------------------------------------------------------------------   
# Exemple papillon
# bleus: voisins
# rouge: point initial
# jaune: point optimisé
#       
#P13  =  Point(1.4265847744427302, 0.3454915028125263, 0.0)
#P22  =  Point(0.9510565162951534, 0.6909830056250525, 0.0)
#P23  =  Point(1.42658477444273, 0.8454915028125263, 0.0)
#P24  =  Point(1.9021130325903068, 0.6909830056250525, 0.0)
#P32  =  Point(0.9510565162951534, 1.1909830056250523, 0.0)
#P33  =  Point(1.42658477444273, 1.0364745084375786, 0.0)
#P34  =  Point(1.9021130325903068, 1.190983005625052, 0.0)
#P43  =  Point(1.42658477444273, 1.5364745084375784, 0.0)
#
#
#newP23=optimisation(P23,P22,P13,P24, 0.5, 0)
#newP33=optimisation(P33,P32,P43,P34, 0.5, 0)
#plt.plot([P32.x, P43.x, P34.x, P24.x, P13.x, P22.x], [P32.y, P43.y, P34.y, P24.y, P13.y, P22.y], 'bo')
##plt.plot([P12.y, P32.x, P13.x, P33.x], [P12.y, P32.y, P13.y, P33.y], 'bo')
#plt.plot([P23.x, P33.x], [P23.y, P33.y], 'ro')
#plt.plot([newP23.x, newP33.x], [newP23.y, newP33.y], 'yo')
#plt.axis([0,2,0,2])
#plt.show()
#plt.figure()