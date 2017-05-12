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
def optimisation(P1,P2,P3,P4,P5, l, e, a, pond=[1,1,0], i=0):
    """
    Calcule la position optimale du point P1 par rapport à ses points
    voisins P2, P3, P4, lorsque la distance désirée entre ces points vaut l
    et que les deux angles formés par ces quatre points vaut a.
    P1, P2, P3, P4 : objets de type Point
    l : distance désirée entre les points
    e : distance idéale avec le voisin "non relié"
    a : angle P2P1P3 et P3P1P4 désiré
    pond : tableau de taille 3 qui contient les coefficients de pondération
            dans l'expression de l'énergie.
            Energie = ponderations[0]*Energie(longueurs)
                        + ponderations[1]*Energie(angles)
                        + ponderations[2]*Energie(ressort fictif)
    i : ne rien mettre, sert à compter le nombre d'appels récursifs effectués
    
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
    oldE = Energie(P1, P2, P3, P4, P5, l, e, a, pond)
#    print("Energie à l'itération ", i, " : ", oldE)
#    print("Position du point à l'itération ", i, " : (", P1.x, ";", P1.y, ";", P1.z, ")")
    newP1=Point(P1.x, P1.y, P1.z) # X(k+1) dans la méthode de Newton
    calculerDerivees(P1, P2, P3, P4, P5, l, e, a, pond) # Calcul des dérivées simples et secondes
    Df = DGradE() # Jacobien du Gradient de E
    f = gradE() # Gradient de E
#    print("Dérivée première de E = ", f)
#    print("Dérivée seeconde de E = ", Df)
#    if(abs(f[0]) > 20000):
#        print("Problème ! Un point déconne.")
#        print("Point à la coordonnée : (", P1.x, ";", P1.y, ";", P1.z, ")")
#        assert(1==0)
    l1 = [Df[0][0], Df[0][1], -f[0]] # Ligne 1 Système de Cramer (ligne 120)
    l2 = [Df[1][0], Df[1][1], -f[1]] # Ligne 2
    res=cramer(l1, l2) # Résolution du système de Cramer
    newP1.x = P1.x + res[0] # X(k+1) = Z + X(k) dans les notes d'Annie
    newP1.y = P1.y + res[1]
    plt.plot([newP1.x], [newP1.y], 'go')
    plt.annotate(i, (P1.x, P1.y))
    if (i==0): # Au moins un tour d'optimisation
        return optimisation(newP1, P2, P3, P4, P5, l, e, a, pond, i+1)
    else:
        newE = Energie(newP1, P2, P3, P4, P5, l, e, a, pond)
        changement = newE - oldE
#        if (changement > 0):
#            # La nouvelle énergie est plus grande que l'ancienne : on a déterioré la situation
#            # On prend donc l'ancien point et on le renvoit
#            print("Energie à l'itération ", i, " : ", oldE, "; arrêt car augmentation de l'énergie. Sinon, vaudrait", newE)
#            return P1
        if (i==10):#(abs(changement) < epsilon):
            #print("on a fait " + str(i) + " appels récursifs.")
            print("Fini après", i, "optimisations ! Energie finale : ", newE)
            return newP1
        else:
            return optimisation(newP1, P2, P3, P4, P5, l, e, a, pond, i+1)

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

def Energie(P1, P2, P3, P4, P5, l, e, a, pond = [1,1,0]):
    """
    Renvoie l'énergie d'un point P1 par rapport à ses voisins P2, P3, P4,
    pour une longueur cible l.
    P1, P2, P3, P4 : objets de type Point
    l : distance désirée entre les points
    e : distance idéale avec le voisin "non relié"
    pond : tableau de taille 3 qui contient les coefficients de pondération
            dans l'expression de l'énergie.
            Energie = ponderations[0]*Energie(longueurs)
                        + ponderations[1]*Energie(angles)
                        + ponderations[2]*Energie(ressort fictif)
    
    Résultat : la valeur de l'énergie
    """
    energie = 0
    if (pond[0] != 0): # Energie des longueurs
        d1 = (P1.distance(P2)**2 - l**2)**2
        d2 = (P1.distance(P3)**2 - l**2)**2
        d3 = (P1.distance(P4)**2 - l**2)**2
        energie += pond[0]*(d1+d2+d3)
    if (pond[1] != 0): # Energie des angles
        N1 = (P3.x-P1.x)*(P2.x-P1.x)+(P3.y-P1.y)*(P2.y-P1.y)+(P3.z-P1.z)*(P2.z-P1.z)
        N2 = (P4.x-P1.x)*(P3.x-P1.x)+(P4.y-P1.y)*(P3.y-P1.y)+(P4.z-P1.z)*(P3.z-P1.z)
        S2 = sqrt((P2.x-P1.x)**2+(P2.y-P1.y)**2+(P2.z-P1.z)**2)
        S3 = sqrt((P3.x-P1.x)**2+(P3.y-P1.y)**2+(P3.z-P1.z)**2)
        S4 = sqrt((P4.x-P1.x)**2+(P4.y-P1.y)**2+(P4.z-P1.z)**2)
        a1 = acos(N1/(S2*S3))
        a2 = acos(N2/(S3*S4))
        energie += pond[1]*((a1-a)**2+(a2-a)**2)
    if (pond[2] != 0): # Energie du ressort fictif
        d4 = (P1.distance(P5)**2 -e**2)**2
        energie += pond[2]*d4
    return energie

derivees = [[0.0, 0.0], [0.0, 0.0, 0.0]]

def calculerDerivees(P1, P2, P3, P4, P5, l, e,  a, pond):
    """
    Calcule et stocke dans la variable globale "derivees" les dérivées simples et
    secondes de l'énergie selon le critère de longueur l, le critère d'angle a,
    et les coefficients de pondération contenus dans le tableau pond.
    
    Résultat : Ne renvoie rien, mais complète la matrice dérivées de la manière suivante :
    derivees[0][0] = dE/dx
    derivees[0][1] = dE/dy
    derivees[1][0] = d²E/dx²
    derivees[1][1] = d²E/dy²
    derivees[1][2] = d²E/dxdy = d²E/dydx
    """
    assert isinstance(P1,Point) 
    assert isinstance(P2,Point) 
    assert isinstance(P3,Point) 
    assert isinstance(P4,Point)
    assert isinstance(P5,Point)
    
    derivees[0][0] = 0
    derivees[0][1] = 0
    derivees[1][0] = 0
    derivees[1][1] = 0
    derivees[1][2] = 0
    
    if (pond[0] != 0): # Energie des longueurs
        
        # dE/dx
        derivees[0][0]= (P1.x-P2.x)*((P1.x-P2.x)**2+(P1.y-P2.y)**2+(P1.z-P2.z)**2-l**2)
        derivees[0][0]+= (P1.x-P3.x)*((P1.x-P3.x)**2+(P1.y-P3.y)**2+(P1.z-P3.z)**2-l**2)
        derivees[0][0]+= (P1.x-P4.x)*((P1.x-P4.x)**2+(P1.y-P4.y)**2+(P1.z-P4.z)**2-l**2)
        derivees[0][0]*= 4*pond[0]
        
        # dE/dy
        derivees[0][1]= (P1.y-P2.y)*((P1.x-P2.x)**2+(P1.y-P2.y)**2+(P1.z-P2.z)**2-l**2)
        derivees[0][1]+= (P1.y-P3.y)*((P1.x-P3.x)**2+(P1.y-P3.y)**2+(P1.z-P3.z)**2-l**2)
        derivees[0][1]+= (P1.y-P4.y)*((P1.x-P4.x)**2+(P1.y-P4.y)**2+(P1.z-P4.z)**2-l**2)
        derivees[0][1]*= 4*pond[0]
        
        # d²E/dx²
        derivees[1][0]= 3*(P1.x-P2.x)**2+(P1.y-P2.y)**2+(P1.z-P2.z)**2-l**2
        derivees[1][0]+= 3*(P1.x-P3.x)**2+(P1.y-P3.y)**2+(P1.z-P3.z)**2-l**2
        derivees[1][0]+= 3*(P1.x-P4.x)**2+(P1.y-P4.y)**2+(P1.z-P4.z)**2-l**2
        derivees[1][0]*= 4*pond[0]
        
        # d²E/dy²
        derivees[1][1]= 3*(P1.y-P2.y)**2+(P1.x-P2.x)**2+(P1.z-P2.z)**2-l**2
        derivees[1][1]+= 3*(P1.y-P3.y)**2+(P1.x-P3.x)**2+(P1.z-P3.z)**2-l**2
        derivees[1][1]+= 3*(P1.y-P4.y)**2+(P1.x-P4.x)**2+(P1.z-P4.z)**2-l**2
        derivees[1][1]*= 4*pond[0]
        
        # d²E/dxdy = d²E/dydx
        derivees[1][2]= (P1.x-P2.x)*(P1.y-P2.y)
        derivees[1][2]+= (P1.x-P3.x)*(P1.y-P3.y)
        derivees[1][2]+= (P1.x-P4.x)*(P1.y-P4.y)
        derivees[1][2]*= 8*pond[0]
    
    if (pond[2] != 0): # Energie du point miroir     
        d = P1.distance(P5)**2 - e**2
        # dérivées ordre 1
        derivees[0][0]+= 4*pond[2]* (P1.x-P5.x)*d
        derivees[0][1]+= 4*pond[2]* (P1.y-P5.y)*d   
        # dérivées ordre 2
        derivees[1][0]+= 4*pond[2]* (2*(P1.x - P5.x)**2 + d)
        derivees[1][1]+= 4*pond[2]* (2*(P1.y - P5.y)**2 + d)
        derivees[1][2]+= 8*pond[2]* (P1.x-P5.x)*(P1.y-P5.y)
    
    if (pond[1] != 0): # Energie des angles
        
        S2 = sqrt((P2.x-P1.x)**2+(P2.y-P1.y)**2+(P2.z-P1.z)**2)
        S3 = sqrt((P3.x-P1.x)**2+(P3.y-P1.y)**2+(P3.z-P1.z)**2)
        S4 = sqrt((P4.x-P1.x)**2+(P4.y-P1.y)**2+(P4.z-P1.z)**2)
        dx_S2 = (P1.x - P2.x)/S2
        dx_S3 = (P1.x - P3.x)/S3
        dx_S4 = (P1.x - P4.x)/S4
        dy_S2 = (P1.y - P2.y)/S2
        dy_S3 = (P1.y - P3.y)/S3
        dy_S4 = (P1.y - P4.y)/S4
        d2x_S2 = (S2-(P1.x - P2.x)*dx_S2)/(S2**2)
        d2y_S2 = (S2-(P1.y - P2.y)*dy_S2)/(S2**2)
        d2xy_S2 = ((P2.x - P1.x)*dy_S2)/(S2**2)
        d2x_S3 = (S3-(P1.x - P3.x)*dx_S3)/(S3**2)
        d2y_S3 = (S3-(P1.y - P3.y)*dy_S3)/(S3**2)
        d2xy_S3 = ((P3.x - P1.x)*dy_S3)/(S3**2)
        d2x_S4 = (S4-(P1.x - P4.x)*dx_S4)/(S4**2)
        d2y_S4 = (S4-(P1.y - P4.y)*dy_S4)/(S4**2)
        d2xy_S4 = ((P4.x - P1.x)*dy_S4)/(S4**2)
        
        N23 = (P3.x-P1.x)*(P2.x-P1.x)+(P3.y-P1.y)*(P2.y-P1.y)+(P3.z-P1.z)*(P2.z-P1.z)
        N34 = (P4.x-P1.x)*(P3.x-P1.x)+(P4.y-P1.y)*(P3.y-P1.y)+(P4.z-P1.z)*(P3.z-P1.z)
        dx_N23 = 2*P1.x - P2.x - P3.x
        dx_N34 = 2*P1.x - P3.x - P4.x
        dy_N23 = 2*P1.y - P2.y - P3.y
        dy_N34 = 2*P1.y - P3.y - P4.y
        d2x_N23 = 2
        d2x_N34 = 2
        d2y_N23 = 2
        d2y_N34 = 2
        d2xy_N23 = 0
        d2xy_N34 = 0
        
        D23 = S2*S3
        D34 = S3*S4
        dx_D23 = dx_S3*S2+dx_S2*S3
        dx_D34 = dx_S4*S3+dx_S3*S4
        dy_D23 = dy_S3*S2+dy_S2*S3
        dy_D34 = dy_S4*S3+dy_S3*S4
        d2x_D23 = d2x_S3*S2 + dx_S3*dx_S2 + dx_S3*dx_S2 + S3*d2x_S2
        d2x_D34 = d2x_S4*S3 + dx_S4*dx_S3 + dx_S4*dx_S3 + S4*d2x_S3
        d2y_D23 = d2y_S3*S2 + dy_S3*dy_S2 + dy_S3*dy_S2 + S3*d2y_S2
        d2y_D34 = d2y_S4*S3 + dy_S4*dy_S3 + dy_S4*dy_S3 + S4*d2y_S3
        d2xy_D23 = d2xy_S3*S2 + dx_S3*dy_S2 + dy_S3*dx_S2 + S3*d2xy_S2
        d2xy_D34 = d2xy_S4*S3 + dx_S4*dy_S3 + dy_S4*dx_S3 + S4*d2xy_S3
        
        Mx23 = D23*dx_N23 - N23*dx_D23
        Mx34 = D34*dx_N34 - N34*dx_D34
        My23 = D23*dy_N23 - N23*dy_D23
        My34 = D34*dy_N34 - N34*dy_D34
        dx_Mx23 = d2x_N23*D23 + dx_N23*dx_D23 - dx_N23*dx_D23 - N23*d2x_D23
        dx_Mx34 = d2x_N34*D34 + dx_N34*dx_D34 - dx_N34*dx_D34 - N34*d2x_D34
        dy_Mx23 = d2xy_N23*D23 + dx_N23*dy_D23 - dy_N23*dx_D23 - N23*d2xy_D23
        dy_Mx34 = d2xy_N34*D34 + dx_N34*dy_D34 - dy_N34*dx_D34 - N34*d2xy_D34
        dy_My23 = d2y_N23*D23 + dy_N23*dy_D23 - dy_N23*dy_D23 - N23*d2y_D23
        dy_My34 = d2y_N34*D34 + dy_N34*dy_D34 - dy_N34*dy_D34 - N34*d2y_D34
        
        A23 = N23/D23
        A34 = N34/D34
        dx_A23 = Mx23/(D23**2)
        dx_A34 = Mx34/(D34**2)
        dy_A23 = My23/(D23**2)
        dy_A34 = My34/(D34**2)
        d2x_A23 = (D23*D23*dx_Mx23 - Mx23*2*D23*dx_D23)/(D23**4)
        d2x_A34 = (D34*D34*dx_Mx34 - Mx34*2*D34*dx_D34)/(D34**4)
        d2y_A23 = (D23*D23*dy_My23 - My23*2*D23*dy_D23)/(D23**4)
        d2y_A34 = (D34*D34*dy_My34 - My34*2*D34*dy_D34)/(D34**4)
        d2xy_A23 = (D23*D23*dy_Mx23 - Mx23*2*D23*dy_D23)/(D23**4)
        d2xy_A34 = (D34*D34*dy_Mx34 - Mx34*2*D34*dy_D34)/(D34**4)
        
        angle23 = acos(A23)
        angle34 = acos(A34)
        dx_angle23 = -(1/sqrt(1-A23*A23))*dx_A23
        dx_angle34 = -(1/sqrt(1-A34*A34))*dx_A34
        dy_angle23 = -(1/sqrt(1-A23*A23))*dy_A23
        dy_angle34 = -(1/sqrt(1-A34*A34))*dy_A34
        d2x_angle23 = (-d2x_A23*sqrt(1-A23*A23) - A23*dx_A23*dx_A23*(1/sqrt(1-A23*A23)))/(1-A23*A23)
        d2x_angle34 = (-d2x_A34*sqrt(1-A34*A34) - A34*dx_A34*dx_A34*(1/sqrt(1-A34*A34)))/(1-A34*A34)
        d2y_angle23 = (-d2y_A23*sqrt(1-A23*A23) - A23*dy_A23*dy_A23*(1/sqrt(1-A23*A23)))/(1-A23*A23)
        d2y_angle34 = (-d2y_A34*sqrt(1-A34*A34) - A34*dy_A34*dy_A34*(1/sqrt(1-A34*A34)))/(1-A34*A34)
        d2xy_angle23 = (-d2xy_A23*sqrt(1-A23*A23) - A23*dx_A23*dy_A23*(1/sqrt(1-A23*A23)))/(1-A23*A23)
        d2xy_angle34 = (-d2xy_A34*sqrt(1-A34*A34) - A34*dx_A34*dy_A34*(1/sqrt(1-A34*A34)))/(1-A34*A34)
        
        # dE/dx
        derivees[0][0]+= 2*(angle23-a)*dx_angle23*pond[1]
        derivees[0][0]+= 2*(angle34-a)*dx_angle34*pond[1]
        
        # dE/dx
        derivees[0][1]+= 2*(angle23-a)*dy_angle23*pond[1]
        derivees[0][1]+= 2*(angle34-a)*dy_angle34*pond[1]
        
        # d²E/dx²
        derivees[1][0]+= (2*dx_angle23*dx_angle23 + 2*(angle23-a)*d2x_angle23)*pond[1]
        derivees[1][0]+= (2*dx_angle34*dx_angle34 + 2*(angle34-a)*d2x_angle34)*pond[1]
        
        # d²E/dy²
        derivees[1][1]+= (2*dy_angle23*dy_angle23 + 2*(angle23-a)*d2y_angle23)*pond[1]
        derivees[1][1]+= (2*dy_angle34*dy_angle34 + 2*(angle34-a)*d2y_angle34)*pond[1]
        
        # d²E/dxdy = d²E/dydx
        derivees[1][2]+= (2*dy_angle23*dx_angle23 + 2*(angle23-a)*d2xy_angle23)*pond[1]
        derivees[1][2]+= (2*dy_angle34*dx_angle34 + 2*(angle34-a)*d2xy_angle34)*pond[1]

def DGradE():
    """
    /!\ Doit être appelé après l'exécution de calculerDerivees(P1,P2,P3,P4,l,a)
    Renvoie le jacobien du gradient de E pour le point P1 et ses vosisins
    P1, P2, P3, P4 avec pour longueur cible l et un angle cible a.
    P1, P2, P3, P4 : objets de type Point
    l : distance désirée entre les points
    a : angle P2P1P3 et P3P1P4 désiré
    
    Résultat : une matrice 2*2
    """
    return[[derivees[1][0], derivees[1][2]], [derivees[1][2], derivees[1][1]]]
    
def gradE():
    """
    /!\ Doit être appelé après l'exécution de calculerDerivees(P1,P2,P3,P4,l,a)
    Renvoie le gradient de E pour le point P1 et ses vosisins
    P1, P2, P3, P4 avec pour longueur cible l et un angle cible a.
    P1, P2, P3, P4 : objets de type Point
    l : distance désirée entre les points
    a : angle P2P1P3 et P3P1P4 désiré
    
    Résultat : un vecteur de dimension 2
    """
    return [derivees[0][0], derivees[0][1]]

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
#P1=Point(1.0/sqrt(2.0), 1.0/sqrt(2.0), 0.0)
#P2=Point(0.0, 0.0, 0.0)
#P3=Point(2.0/sqrt(2.0), 0.0, 0.0)
#P4=Point(1.0/sqrt(2.0), 1.0+1.0/sqrt(2.0), 0.0)

#P1=Point(0.5+0.2, sqrt(3)/6+0.2, 0.0)
#P2=Point(0.0, 0.0, 0.0)
#P3=Point(0.5, sqrt(3)/2, 0.0)
#P4=Point(1.0, 0.0, 0.0)
#
#N1 = (P3.x-P1.x)*(P2.x-P1.x)+(P3.y-P1.y)*(P2.y-P1.y)+(P3.z-P1.z)*(P2.z-P1.z)
#N2 = (P4.x-P1.x)*(P3.x-P1.x)+(P4.y-P1.y)*(P3.y-P1.y)+(P4.z-P1.z)*(P3.z-P1.z)
#S2 = sqrt((P2.x-P1.x)**2+(P2.y-P1.y)**2+(P2.z-P1.z)**2)
#S3 = sqrt((P3.x-P1.x)**2+(P3.y-P1.y)**2+(P3.z-P1.z)**2)
#S4 = sqrt((P4.x-P1.x)**2+(P4.y-P1.y)**2+(P4.z-P1.z)**2)
#a1 = acos(N1/(S2*S3))
#a2 = acos(N2/(S3*S4))
#
#l=sqrt(3)/3
#a = 2*pi/3
#
#print("")
#print("Point initial :")
#print("a1 :", a1-a, "| a2 :", a2-a, "| 2pi/3 :", a)
#print("L1 :", P1.distance(P2)-l, "| L2 :", P1.distance(P3)-l, "| L3 :", P1.distance(P4)-l, "| L :", l)
#print("")
#
#newP1=optimisation(P1,P2,P3,P4, l, a, [0, 1, 0])
#
#plt.plot([P2.x, P3.x, P4.x], [P2.y, P3.y, P4.y], 'bo')
#plt.plot([P1.x], [P1.y], 'ro')
#
#P1 = newP1
#
#N1 = (P3.x-P1.x)*(P2.x-P1.x)+(P3.y-P1.y)*(P2.y-P1.y)+(P3.z-P1.z)*(P2.z-P1.z)
#N2 = (P4.x-P1.x)*(P3.x-P1.x)+(P4.y-P1.y)*(P3.y-P1.y)+(P4.z-P1.z)*(P3.z-P1.z)
#S2 = sqrt((P2.x-P1.x)**2+(P2.y-P1.y)**2+(P2.z-P1.z)**2)
#S3 = sqrt((P3.x-P1.x)**2+(P3.y-P1.y)**2+(P3.z-P1.z)**2)
#S4 = sqrt((P4.x-P1.x)**2+(P4.y-P1.y)**2+(P4.z-P1.z)**2)
#a1 = acos(N1/(S2*S3))
#a2 = acos(N2/(S3*S4))
#
#print("")
#print("Point final :")
#print("a1-a :", a1-a, "| a2-a :", a2-a, "| 2pi/3 :", a)
#print("L1-L :", P1.distance(P2)-l, "| L2-L :", P1.distance(P3)-l, "| L3-L :", P1.distance(P4)-l, "| L :", l)
#print("")
#
#plt.plot([newP1.x], [newP1.y], 'yo')
#plt.axis('equal')
#plt.show()
#print("Point optimise attendu : (", 0.5, ";", sqrt(3)/6, ")")
#print("Point optimise trouve : (", newP1.x, ";", newP1.y, ")")

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
#newP23=optimisation(P23,P22,P13,P24, 0.5, pi/2.5)
#newP33=optimisation(P33,P32,P43,P34, 0.5, pi/2.5)
#plt.plot([P32.x, P43.x, P34.x, P24.x, P13.x, P22.x], [P32.y, P43.y, P34.y, P24.y, P13.y, P22.y], 'bo')
##plt.plot([P12.y, P32.x, P13.x, P33.x], [P12.y, P32.y, P13.y, P33.y], 'bo')
#plt.plot([P23.x, P33.x], [P23.y, P33.y], 'ro')
#plt.plot([newP23.x, newP33.x], [newP23.y, newP33.y], 'yo')
#plt.axis([0,2,0,2])
#plt.show()
#plt.figure()
       
###############################################################################
# Exemple pour tester l'ajout du point mirroir dans le calcul de l'énergie
###############################################################################
#l=1.0
#a = pi/2.5
#e = l - 2*l*cos(a)
#
#P1=Point(0, l-l*cos(a), 0.0)
#P2=Point(0.0, 0.0, 0.0)
#P3=Point(l*sin(a), l*cos(a)-l, 0.0)
#P4=Point(2*l*sin(a), 0.0, 0.0)
#P5=Point(l*sin(a), l-l*cos(a), 0.0)
#P =Point(l*sin(a), l*cos(a), 0.0)
#
#P.afficherSegment(P5)
#P.afficherSegment(P2)
#P.afficherSegment(P3)
#P.afficherSegment(P4)
#
#newP1=optimisation(P1,P2,P3,P4, P5, l, e, a, [0.5, 0, 0.5])
#
#plt.plot([P2.x, P3.x, P4.x, P5.x, P.x], [P2.y, P3.y, P4.y, P5.y, P.y], 'bo')
#plt.plot([P1.x], [P1.y], 'ro')
#
#P1 = newP1
#
#plt.plot([newP1.x], [newP1.y], 'yo')
#plt.axis('equal')
#plt.show()      
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       