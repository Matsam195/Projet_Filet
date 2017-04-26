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
cmap = plt.cm.inferno

class ListePoints: 

    def afficher(self):
        #mpl.rcParams['legend.fontsize'] = 10

        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.set_xlim3d(0, 12)
        ax.set_ylim3d(0, 12)
        ax.set_zlim3d(-1,1)
       
        # si le nb de papillons verticaux est pair, 
        # alors il existe un point fantome 
#        for j in range(0, self.m):
#            for i in range(0, self.n):
#                self.get(i,j).afficherPoint()   
#                if (i > 0 and i < self.n-1 and j > 0 and j < self.m-1) :
#                    l = self.getVoisins(i,j)    
#                    for voisin in range(0, 3) :
#                        l[voisin].afficherSegment(self.get(i,j))
        for i in range(1, self.n-1):
            for j in range(1, self.m-1):
                P = self.get(i,j)
                if (not self.estBord(P)):
                    for v in self.getVoisins(i, j):
                        x = [P.x, v.x]
                        y = [P.y, v.y]
                        z = [P.z, v.z]
                        ax.plot(x,y,z, color = cmap(norm(P.distance(v))))       
        #plt.show()
                
    def get(self, i, j):
        assert((i >= 0) and (j >= 0))
        assert ((i <= self.n-1) and (j <= self.m-1))
        # élimination des points fantomes :        
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
        
    # on ne peut pas demander le voisin d'un bord pour le moment
    # évite la gestion des fantômes aussi
    # les voisins sont donnés par ordre de j croissant
    def getVoisins(self, i, j) :
        assert ((i > 0) and (j > 0))
        assert ((i < self.n-1) and (j < self.m-1))
        listeVoisins = []
        listeVoisins.append(self.get(i, j-1))
        if (i % 2) == (j % 2): # flèche vers le bas 
            listeVoisins.append(self.get(i+1,j))
        else :
            listeVoisins.append(self.get(i-1, j))
        listeVoisins.append(self.get(i, j+1))
        return listeVoisins
#    def setL(self, i, j, val):
#        assert(i>=0 and j>=0)        
#        self.pts[i + j*(self.n)] = val
#        # gestion des points fantomes : 
#        if (i == self.n and j == 0) :
#            if self.mailleN % 2 == 0:
#                self.pts[i + j*(self.n)] = Point(-1,-1)                        
#        if (i == 0 and j == self.m) :
#            if (self.mailleM % 2 == 0):
#                self.pts[i + j*(self.n)] = Point(-1,-1)
              
    def projection(self, surface):
        for i in range(0, self.n):
            for j in range(0, self.m):
                x = self.get(i,j).x
                y = self.get(i,j).y
                assert isinstance(surface(x,y),Point) 
                self.pts[i+j*(self.n)] = surface(x,y) 
    
    def estBord(self, p):
        return (p.x == 0 or p.y == 0 or p.x == self.n or p.y == self.m)
        
        
    
        

    """ Initialisation à partir d'une maille
        n et m sont calculés à partir de cette maille pour plus de clarté    
    """ 
    def __init__(self, maille):
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
            print(i)
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
            #    liste.append(maille.get(0,j).sm)
                    
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
            
        #print(nb_pts)
            
        self.pts = liste