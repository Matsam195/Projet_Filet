# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 12:15:29 2017

@author: Mégane B
"""

import numpy as np
from Point import *
from Papillon import *
from Maille import *
from interpolation import *


#affichage 3d
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D

L = 0.5

norm = mpl.colors.Normalize(vmin=L, vmax=L*1.5)
#cmapPlus = plt.cm.inferno
#cmapMoins = plt.cm.cubehelix_r

def make_colormap(seq):
    """Return a LinearSegmentedColormap
    seq: a sequence of floats and RGB-tuples. The floats should be increasing
    and in the interval (0,1).
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
        # si le nb de papillons verticaux est pair, 
        # alors il existe un point fantome 
#        for j in range(0, self.m):
#            for i in range(0, self.n):
#                self.get(i,j).afficherPoint()   
#                if (i > 0 and i < self.n-1 and j > 0 and j < self.m-1) :
#                    l = self.getVoisins(i,j)    
#                    for voisin in range(0, 3) :
#                        l[voisin].afficherSegment(self.get(i,j))
        
        #sert à fixer la valeur de norme e couleur
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
                            
        if (maxL-minL < 0.0000000000001):
            maxL = L*1.5
        
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
        # élimination des points fantomes s'ils existent:        
        if (i == self.n and j == 0) :
            if self.mailleN % 2 == 0:
                assert isinstance(self.pts[0],Point) 
                return self.pts[0]                        
        if (i == 0 and j == self.m) :
            if (self.mailleM % 2 == 0):
                assert isinstance(self.pts[0],Point) 
                return self.pts[0]
        assert isinstance(self.pts[i + j*(self.n)],Point)                
        return self.pts[i + j*(self.n)]
        

    # les voisins sont donnés par ordre de j croissant
    def getVoisins(self, i, j) :
        """renvoie les voisins d'un point
        (principalement utilisées pour l'optimisation)
        i : ligne du point
        j : colonne 
        renvoie une liste de 4 voisins :
            les trois premiers sont les voisins directs triés par colonne croissante
            le dernier est le voisin non relié (symétrie horizontale)"""
        assert ((i > 0) and (j > 0))
        assert ((i < self.n-1) and (j < self.m-1))
        listeVoisins = []
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
            if (self.get(i,j-1).x != -1):
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
                self.pts[i+j*(self.n)] = surface(x,y) 
    
    def estBord(self, p):
        return (p.x == 0 or p.y == 0 or p.x == self.n or p.y == self.m)
        
        
    
        

 
    def __init__(self, maille):    
        """ Initialisation d'une liste de points à partir d'une maille
            une liste de points contient :
            - n points en hauteur
            - m points en largeur
            n et m sont calculés à partir de la maille en entrée pour plus de clarté
            si des points sont manquants aux extremités, on ajoute des points "fantômes"
            de coordonnées (-1,-1,0), il faudra les considérer dans les fonctions de
            plus haut niveau
        """
        self.n = maille.n + 1 # n le nombre de points en hauteur
        self.mailleN = maille.n
        self.m = maille.m * 2 + 2 # m le nombre de points en largeur 
        self.mailleM = maille.m
        
        # initialisation de la liste de points à partir de la maille :
        liste = []
        nb_pts = 0
        pair = (maille.n % 2) == 0
        fantome = Point(-1,-1, 0)
        
        # on trace les deux premières colonnes :
        for i in range(0,maille.n,2):
            liste.append(maille.get(i,0).so)
            liste.append(maille.get(i,0).no)
            nb_pts = nb_pts + 2        
        
        # ajout d'un point encore au dessus 
        if pair:
            liste.append(fantome)
            nb_pts = nb_pts +1
        #else :
            # rien car les papillons sont déjà ajoutés en entier
                
        # on compte le point de la première ligne :
        for i in range(0,maille.n,2):        
            liste.append(maille.get(i,0).sm)
            liste.append(maille.get(i,0).nm)
            nb_pts = nb_pts + 2

        if pair:
            liste.append(maille.get(maille.n-1,0).no)
            nb_pts = nb_pts + 1
        
        # on trace le corps, à chaque coup on a deux colonnes créées :
        j = 0
        while j < maille.m:
            for i in range(0,maille.n,2):
                liste.append(maille.get(i,j).se)
                liste.append(maille.get(i,j).ne)
                nb_pts = nb_pts + 2
                
            # ajout d'un point encore au dessus 
            if pair:
                liste.append(maille.get(maille.n-1, j).nm)
                nb_pts = nb_pts +1
                
            # ajout du point de la première ligne éventuellemnt
            if maille.m > j +1: 
                liste.append(maille.get(0,j+1).sm)
                nb_pts = nb_pts +1
            else : 
                liste.append(fantome)
                nb_pts = nb_pts + 1
                
            for i in range(1,maille.n,2):
                liste.append(maille.get(i,j).se)
                liste.append(maille.get(i,j).ne)
                nb_pts = nb_pts + 2
            
            # Ajout du point en bas à droite de la grille
            if not pair :
                if maille.m > j + 1:
                    liste.append(maille.get(maille.n-1, j+1).nm)
                    nb_pts = nb_pts + 1                     
                else:
                    liste.append(fantome)
                    nb_pts = nb_pts +1
                
            j = j + 1    
            
            if not(j >= maille.m):
                for i in range(0,maille.n,2):
                    liste.append(maille.get(i,j).se)
                    liste.append(maille.get(i,j).ne)
                    nb_pts = nb_pts + 2
                
                # Ajout éventuel d'un point en haut de la grille 
                if pair :
                    liste.append(maille.get(maille.n-1,j).nm)
                    nb_pts = nb_pts + 1
                # ajout du point de la première ligne
                if maille.m > j +1: 
                    liste.append(maille.get(0,j+1).sm)
                    nb_pts = nb_pts +1
                else : 
                    liste.append(fantome)
                    nb_pts = nb_pts + 1                
                
                for i in range(1,maille.n,2):
                    liste.append(maille.get(i,j).se)
                    liste.append(maille.get(i,j).ne)
                    nb_pts = nb_pts + 2

                if not pair :
                    if maille.m > j + 1:
                        liste.append(maille.get(maille.n-1, j+1).nm)
                        nb_pts = nb_pts + 1                     
                    else:
                        liste.append(fantome)
                        nb_pts = nb_pts +1                
                
                j = j+1 
                
        if not pair:
            liste.append(fantome)
            
        self.pts = liste