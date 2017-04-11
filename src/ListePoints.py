# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 12:15:29 2017

@author: Mégane B
"""

import numpy as np
from Point import *
from Papillon import *
from Maille import *


class ListePoints: 

    def afficher(self):
        print("taille : ")
        print(self.n)
        print(self.m)        
        # si le nb de papillons verticaux est pair, 
        # alors il existe un point fantome 
        for j in range(self.m):
            for i in range(self.n):
                print("coord : ", i,j) 
                self.get(i,j).afficherPoint()                   
                
    def get(self, i, j):
        assert((i >= 0) and (j >= 0))
        # élimination des points fantomes :        
        if (i == self.n and j == 0) :
            if self.mailleN % 2 == 0:
                return self.pts[0]                        
        if (i == 0 and j == self.m) :
            if (self.mailleM % 2 == 0):
                return self.pts[0]
        return self.pts[i + j*(self.n)]
        
    def getVoisin(self, i, j) :
        assert ((i >= 0) and (j >= 0))
        assert ((i < self.n) and (j < self.m))
        listeVoisins = []
            
        # Gestion renvoi des voisins
        listeVoisins.append()
        
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
                

    """ Initialisation à partir d'une maille
        n et m sont calculés à partir de cette maille pour plus de clarté    
    """ 
    def __init__(self, maille):
        self.n = maille.n + 1 
        self.mailleN = maille.n
        self.m = maille.m * 2 + 2
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
            
        print(nb_pts)
            
        self.pts = liste