# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 11:01:12 2017

@author: Annie
"""

from math import sqrt
import matplotlib.pyplot as plt
from Point import *
from annotation3D import annotate3D

####################################################################
# PARAMETRES D'OPTIMISATION

# Marge d'écart autorisée pour considérer optimisation finie
epsilon = 0.1 

# Nombre d'itérations maximales autorisées
nbIteMax = 50

####################################################################
# PARAMETRES ET VARIABLES POUR LE GRAPH D'ENERGIE
# (ne pas toucher)
minX=0
maxX=0
minY=0
maxY=0
xs=[]
ys=[]
zs=[]
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d') 

#####################################################################
#                     FONCTION PRINCIPALE
def optimisation(P1, P2, P3, P4, P5='no value', pond=[1,0.5,1], l=1, e=1, a=1, graph=False, i=0):
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
    graph : affiche le graphique de l'énergie selon (x,y) et les points
            calculés à chaque itération
    i : ne rien mettre, sert à compter le nombre d'appels récursifs effectués
    
    Résultat : un Point qui est la nouvelle position optimisée de P1
    """
    
    # vérification des paramètres
    assert isinstance(P1,Point) 
    assert isinstance(P2,Point) 
    assert isinstance(P3,Point) 
    assert isinstance(P4,Point) 
    if (pond[2]!=0):
        assert isinstance(P5,Point)    

    # paramètres généraux
    global epsilon
    global nbIteMax
    
    # paramètres pour le graphique
    global xs
    global ys
    global zs
    global minX
    global maxX
    global minY
    global maxY
    global ax
    global fig
    # initialisation pour le graphique
    if (graph==True and i==0):
        print("allo1")
        minX=P1.x
        maxX=P1.x
        minY=P1.y
        maxY=P1.y
        xs.append(P1.x)
        ys.append(P1.y)
        zs.append(Energie(P1, P2, P3, P4, P5, pond, l, e, a))
        annotate3D(ax, s='P1', xyz=(P1.x, P1.y, Energie(P1,P2,P3,P4,P5,pond=pond, l=l, e=e, a=a)), fontsize=10, xytext=(-3,3), textcoords='offset points', ha='right',va='bottom')
    
    
    # on teste qu'on n'a pas fait trop d'appels
    if i>nbIteMax:
        #print("Newton : ça n'a pas trop l'air de converger...")
        return P1
    
    # Calcul du nouveau point
    oldE = Energie(P1, P2, P3, P4, P5, pond=pond, l=l, e=e, a=a)
    newP1=Point(P1.x, P1.y, P1.z) # X(k+1) dans la méthode de Newton
    calculerDerivees(P1, P2, P3, P4, P5, pond=pond, l=l, e=e, a=a) # Calcul des dérivées simples et secondes
    Df = DGradE() # Jacobien du Gradient de E
    f = gradE() # Gradient de E
    l1 = [Df[0][0], Df[0][1], -f[0]] # Ligne 1 Système de Cramer (ligne 120)
    l2 = [Df[1][0], Df[1][1], -f[1]] # Ligne 2
    res=cramer(l1, l2) # Résolution du système de Cramer
    newP1.x = P1.x + res[0] # X(k+1) = Z + X(k)
    newP1.y = P1.y + res[1]
    
    
    # Mise à jour du graphique
    if (graph==True):
        if (newP1.x < minX):
            minX=newP1.x
        if (newP1.x > maxX):
                maxX=newP1.x
        if (newP1.y < minY):
            minY=newP1.y
        if (newP1.y > maxY):
            maxY=newP1.y
        xs.append(newP1.x)
        ys.append(newP1.y)
        zs.append(Energie(newP1,P2,P3,P4,P5,pond,l,e,a))
        annotate3D(ax, s=str(i), xyz=(newP1.x, newP1.y, Energie(newP1,P2,P3,P4,P5,pond,l,e,a)), fontsize=10, xytext=(-3,3), textcoords='offset points', ha='right',va='bottom')    
    
    
    
    if (i==0): # Au moins un tour d'optimisation
        return optimisation(newP1, P2, P3, P4, P5, pond=pond, l=l, e=e, a=a, graph=graph, i=i+1)
    else:
        newE = Energie(newP1, P2, P3, P4, P5, pond=pond, l=l, e=e, a=a)
        changement = newE - oldE
#        if (changement > 0):
#            # La nouvelle énergie est plus grande que l'ancienne : on a déterioré la situation
#            # On prend donc l'ancien point et on le renvoit
#            print("Energie à l'itération ", i, " : ", oldE, "; arrêt car augmentation de l'énergie. Sinon, vaudrait", newE)
#            return P1
        if (abs(changement) < epsilon):
#            print("Fini après", i, "optimisations ! Energie finale : ", newE)
            if (graph==True):
                # recalibrage de l'échelle
                minX=minX-(maxX-minX)
                maxX=maxX+(maxX-minX)
                minY=minY-(maxY-minY)
                maxY=maxY+(maxY-minY)
                # affichage de l'énergie sur une grille
                X=[]
                Y=[]
                Z=[]
                N=20
                for i in range(0,N):
                    x=[]
                    y=[]
                    z=[]
                    for j in range(0,N):
                        coordx=minX+(i*(maxX-minX)/N)
                        coordy=minY+(j*(maxY-minY)/N)
                        x.append(coordx)
                        y.append(coordy)
                        P1.x=coordx
                        P1.y=coordy
                        z.append(Energie(P1, P2, P3, P4, P5, pond, l, e, a))
                        X.append(x)
                        Y.append(y)
                        Z.append(z)
                print(xs)
                print(ys)
                print(zs)
                ax.scatter(xs, ys, zs, c='r', marker='o')
                ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1)
                plt.show()
            return newP1
        else:
            return optimisation(newP1, P2, P3, P4, P5, pond=pond, l=l, e=e, a=a, graph=graph, i=i+1)

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

def Energie(P1, P2, P3, P4, P5, pond, l, e, a):
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

def calculerDerivees(P1, P2, P3, P4, P5, pond, l, e, a):
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
    
