
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 12:15:29 2017

@author: Mégane B
"""

import numpy as np
from Point import *
from interpolation import *

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D

L = 0.5

################################################################################
#modules d'affichage

def make_colormap(seq):
    """Renvoie une LinearFragmented COlormap
    seq: une sequence de floats et RGB-tuples.Les floats doivent être croissants
   et dans l'intervalle (0,1).
    """
    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
    return mpl.colors.LinearSegmentedColormap('CustomMap', cdict)


c = mpl.colors.ColorConverter().to_rgb
cmapPlus = make_colormap(
    [c('black'), c('orange'), 0.10, c('orange'), c('red'), 0.65, c('red')])
cmapMoins= make_colormap(
    [c('blue'), c('purple'), 0.45, c('purple'), c('black'), 0.90, c('black')])

class ListePoints: 

    def afficher(self):
        #mpl.rcParams['legend.fontsize'] = 10

        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.set_xlim3d(-6, 12)
        ax.set_ylim3d(-6, 12)
        ax.set_zlim3d(-9,9)
        
        #sert à fixer automatiquement la valeur de norme de couleur
        #on cherche le min et le max
        maxL = L
        minL = L
        for i in range(0, self.n):
            for j in range(0, self.m):
                P = self.get(i,j)
                for v in self.getVoisinsAffichage(i, j):
                    if(maxL < P.distance(v)):
                        maxL = P.distance(v)
                    if(minL > P.distance(v)):
                        minL = P.distance(v) 
                            
        if (maxL-L < 0.000000001):
            maxL = L*1.25
        if (L-minL < 0.000000001):
            minL = L*0.75        
        normPlus = mpl.colors.Normalize(vmin=L, vmax=maxL)
        normMoins = mpl.colors.Normalize(vmin=minL, vmax=L)
                
        for i in range(0, self.n):
            for j in range(0, self.m):
                P = self.get(i,j)
                for v in self.getVoisinsAffichage(i, j):
                    if v.x == -1:
                        print("voisin bizarre de ",i,j)
                    x = [P.x, v.x]
                    y = [P.y, v.y]
                    z = [P.z, v.z]
                    if (P.distance(v) > L):
                        ax.plot(x,y,z, color = cmapPlus(normPlus(P.distance(v)))) 
                    else:
                        ax.plot(x,y,z, color = cmapMoins(normMoins(P.distance(v)))) 
        
        ax1 = fig.add_axes([0.01, 0.3, 0.05, 0.3 ])    
        mpl.colorbar.ColorbarBase(ax1, cmap=cmapPlus, norm=normPlus)
        ax2 = fig.add_axes([0.01, 0.1, 0.05, 0.2])    
        mpl.colorbar.ColorbarBase(ax2, cmap=cmapMoins, norm=normMoins)
        plt.show()
                
    def get(self, i, j):
        assert((i >= 0) and (j >= 0))
        assert ((i <= self.n-1) and (j <= self.m-1))       
        return self.pts[i*self.m + j]

    # les voisins sont donnés par ordre de j croissant
    def getVoisins(self, i, j) :
        """renvoie les voisins d'un point
        (principalement utilisées pour l'optimisation)
        i : ligne du point
        j : colonne 
        renvoie une liste de 4 voisins :
            les trois premiers sont les voisins directs triés par colonne croissante
            le dernier est le voisin non relié (symétrie horizontale)"""
        assert ((i >= 0) and (j >= 0))
        assert ((i <= self.n-1) and (j <= self.m-1))
        current = self.get(i,j)
        listeVoisins = []
        #points intérieurs
        if (i>0 and j > 0 and i < self.n -1 and j < self.m -1):
            listeVoisins.append(self.get(i, j-1))
            if (i % 2) == (j % 2): # flèche vers le bas 
                listeVoisins.append(self.get(i+1,j))
            else :
                listeVoisins.append(self.get(i-1, j))
            listeVoisins.append(self.get(i, j+1))
            # Renvoie le point mirroir :
            if (i % 2) == (j % 2): # flèche vers le bas 
                listeVoisins.append(self.get(i-1,j))
            else :
                listeVoisins.append(self.get(i+1, j))
        
        # Gestion de tous les cas de bord
        elif (i==0 and j >0 and j < self.m -1):
            listeVoisins.append(self.get(i, j-1))
            if (i % 2) == (j % 2): # flèche vers le bas 
                listeVoisins.append(self.get(i+1,j))
            else :
                #n'annule que l'énergie avec longueurs
                listeVoisins.append(Point(current.x, current.y-L, current.z))
            if self.get(i,j+1).x!=-1 :     
                listeVoisins.append(self.get(i, j+1))
            else:
                #point fantôme. n'annule que l'énergie avec les longueurs
                listeVoisins.append(Point(current.x+L, current.y, current.z))
            # Renvoie le point mirroir :
            if (i % 2) == (j % 2): # flèche vers le bas 
                #n'annule que l'énergie avec longueurs
                listeVoisins.append(Point(current.x, current.y-L, current.z))
            else :
                listeVoisins.append(self.get(i+1,j))


        elif (j==0 and i >0 and i < self.n -1):
            #virtuel
            listeVoisins.append(Point(current.x-L, current.y, current.z))
            if (i % 2) == (j % 2): # flèche vers le bas 
                listeVoisins.append(self.get(i+1,j))
            else :
                listeVoisins.append(self.get(i-1, j))
            listeVoisins.append(self.get(i, j+1))
            # Renvoie le point mirroir :
            if (i % 2) == (j % 2): # flèche vers le bas 
                listeVoisins.append(self.get(i-1,j))
            else :
                listeVoisins.append(self.get(i+1, j))
        
        elif (j==self.m-1 and i >0 and i < self.n -1):
            listeVoisins.append(self.get(i, j-1))
            if (i % 2) == (j % 2): # flèche vers le bas 
                if (self.get(i+1,j).x != -1):
                    listeVoisins.append(self.get(i+1,j))
                else:
                    #Point fantôme
                    listeVoisins.append(Point(current.x, current.y+L, current.z))
            else:
                listeVoisins.append(self.get(i-1, j))
            listeVoisins.append(Point(current.x+L, current.y, current.z))
            # Renvoie le point mirroir :
            if (i % 2) == (j % 2): # flèche vers le bas 
                listeVoisins.append(self.get(i-1, j))
            else: 
                if (self.get(i+1,j).x != -1):
                    listeVoisins.append(self.get(i+1,j))
                else:
                    #Point fantôme
                    listeVoisins.append(Point(current.x, current.y+L, current.z))   
        
        elif (i==self.n-1 and j >0 and j < self.m -1): 
            if (self.get(i,j-1).x != -1):
                listeVoisins.append(self.get(i, j-1))
            else:
                listeVoisins.append(Point(current.x -L, current.y, current.z))
            
            if ((i % 2) == (j % 2)): # flèche vers le bas 
                listeVoisins.append(Point(current.x, current.y+L, current.z))
            else:
                listeVoisins.append(self.get(i-1, j))

            if (self.get(i,j+1).y != -1):    
                listeVoisins.append(self.get(i, j+1))
            else:
                listeVoisins.append(Point(current.x+L, current.y, current.z))
            # Renvoie le point mirroir :
            if ((i % 2) == (j % 2)): # flèche vers le bas 
                listeVoisins.append(self.get(i-1, j))
            else:
                listeVoisins.append(Point(current.x, current.y+L, current.z))
        
        elif (i==0 and j==0):
            listeVoisins.append(Point(current.x-L, current.y, current.z))
            listeVoisins.append(self.get(i+1, j)) #note : même parité de i et j
            listeVoisins.append(self.get(i, j+1))
            listeVoisins.append(Point(current.x-L, current.y, current.z))
        
        elif (i==0 and j==self.m-1 and current.x != -1):
            listeVoisins.append(self.get(i, j-1))
            if ((i % 2) == (j % 2)): # flèche vers le bas 
                listeVoisins.append(self.get(i+1,j))
            else: 
                listeVoisins.add(Point(current.x, current.y-L, current.z))
            listeVoisins.append(Point(current.x+L, current.y, current.z))
            if ((i % 2) == (j % 2)): # flèche vers le bas 
                listeVoisins.add(Point(current.x, current.y-L, current.z))
            else: 
                listeVoisins.append(self.get(i+1,j))
            

            
        elif(i==self.n-1 and j==0 and current.x != -1):
            listeVoisins.append(Point(current.x-L, current.y, current.z))
            if ((i % 2) == (j % 2)): # flèche vers le bas 
                listeVoisins.append(Point(current.x, current.y+L, current.z))
            else: 
                listeVoisins.append(self.get(i-1,j))
            listeVoisins.append(self.get(i, j+1))
            if not((i % 2) == (j % 2)): # flèche vers le bas 
                listeVoisins.append(Point(current.x, current.y+L, current.z))
            else: 
                listeVoisins.append(self.get(i-1,j))
            
        elif(i==self.n-1 and j == self.m-1 and current.x != -1):
            listeVoisins.append(self.get(i,j-1))
            if ((i % 2) == (j % 2)): # flèche vers le bas 
                listeVoisins.append(Point(current.x, current.y+L, current.z))
            else: 
                listeVoisins.add(self.get(i-1,j))
                listeVoisins.append(self.get(i, j+1))
            listeVoisins.append(Point(current.x+L, current.y, current.z))
            if not((i % 2) == (j % 2)): # flèche vers le bas 
                listeVoisins.append(Point(current.x, current.y+L, current.z))
            else: 
                listeVoisins.append(self.get(i-1,j))
        return listeVoisins
        
        
    def getVoisinsAffichage(self, i, j) :
        """Cette fonction renvoie les voisins de chaque point pour les afficher
            à la différence de la fonction ci dessus, elle renvoie les voisins 
            liés au sommet et gère le cas complexe des bords 
            i : ligne
            j : colonne
            renvoie une liste de 2 à 3 points voisins (reliés au point entré)"""
        assert ((i >= 0) and (j >= 0))
        assert ((i <= self.n-1) and (j <= self.m-1))
        listeVoisins = []
        # Cas classique d'un point au centre de la maille
        if (i>0 and j > 0 and i < self.n -1 and j < self.m -1):            
            listeVoisins.append(self.get(i, j-1))
            if (i % 2) == (j % 2): # flèche vers le bas 
                listeVoisins.append(self.get(i+1,j))
            else :
                listeVoisins.append(self.get(i-1, j))
            listeVoisins.append(self.get(i, j+1))        

        # Gestion de tous les cas de bord
        elif (i==0 and j >0 and j < self.m -1):
            listeVoisins.append(self.get(i, j-1))
            if (i % 2) == (j % 2): # flèche vers le bas 
                listeVoisins.append(self.get(i+1,j))
            if (self.get(i,j+1).x != -1):
                listeVoisins.append(self.get(i, j+1))

        elif (j==0 and i >0 and i < self.n -1):
            if (i % 2) == (j % 2): # flèche vers le bas 
                listeVoisins.append(self.get(i+1,j))
            else :
                listeVoisins.append(self.get(i-1, j))
            listeVoisins.append(self.get(i, j+1))
        
        elif (j==self.m-1 and i >0 and i < self.n -1):
            listeVoisins.append(self.get(i, j-1))
            if (i % 2) == (j % 2): # flèche vers le bas 
                if (self.get(i+1,j).x != -1):
                    listeVoisins.append(self.get(i+1,j))
            else :
                listeVoisins.append(self.get(i-1, j))
        
        elif (i==self.n-1 and j >0 and j < self.m -1): 
            listeVoisins.append(self.get(i, j-1))
            if not((i % 2) == (j % 2)): # flèche vers le bas 
                listeVoisins.append(self.get(i-1, j))
            if (self.get(i,j+1).y != -1):    
                listeVoisins.append(self.get(i, j+1))
                
        return listeVoisins

              
    def projection(self, surface):
        for i in range(0, self.n):
            for j in range(0, self.m):
                x = self.get(i,j).x
                y = self.get(i,j).y
                assert isinstance(surface(x,y),Point) 
                self.pts[i*self.m + j] = surface(x,y) 
    
    def estBord(self, p):
        return (p.x == 0 or p.y == 0 or p.x == self.n or p.y == self.m)
        
        
    
        

 
    def __init__(self, n, m, l, a, origine=Point(0,0,0)):    
        """ Initialisation d'une liste de points 
            - n : nombre de papillons en hauteur         
            - m : idem en largeur
            - l longueur des côtés
            - a angle 
            - origine de la maille 
            une liste de points contient :
            - n : points en hauteur
            - m : points en largeur
            - n_pap : le nombre de papillons en hauteur
            - m_pap : en largeur
            - pts : liste des points de la maille
            n et m sont calculés à partir de la maille en entrée pour plus de clarté
            si des points sont manquants aux extremités, on ajoute des points "fantômes"
            de coordonnées (-1,-1,0), il faudra les considérer dans les fonctions de
            plus haut niveau
        """
        assert isinstance(origine, Point)          
        self.n = n + 1      # n le nombre de points en hauteur
        self.m = m * 2 + 2  # m le nombre de points en largeur 
        self.n_pap = n        
        self.m_pap = m
        
        # initialisation de la liste de points à partir de la maille :
        liste = []
        pair = (n % 2) == 0
        fantome = Point(-1,-1, 0)
        x = origine.x
        y = origine.y        
        
        # on trace le coeur de la maille       
        hmoy = l - l*cos(a)
        # on va tracer chaque ligne, on considère le milieu et pour avoir l'alternance
        # on utilise la parité de l'indice
        for i in range(0, self.n): #range(1, self.n-1):
            signe = 2*(i%2)-1
            for j in range(0, self.m):
                liste.append(Point( x + j*l*sin(a), 
                                    y + l*cos(a)/2 + i*hmoy + signe*l*cos(a)/2,
                                    0))
                signe = - signe

        self.pts = liste
        
        # On modifie les points fantomes :
        self.pts[self.m -1] = fantome
        if pair:
            self.pts[(self.n-1)*(self.m)] = fantome
        else :
            self.pts[self.n*self.m -1] = fantome        
                    

