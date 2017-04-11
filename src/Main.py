# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 12:01:39 2017

@author: batim
"""

from math import *
from Point import *
from Papillon import *
from Maille import *
from ListePoints import *

angle = pi/2.5
# On génère un nombre fixe de papillons 
maille = Maille(3,2)

# Création de l'origine - 1er papillon en (0,0)
origine = Point(0, 0, 0)
premierPapillon = Papillon(origine, 1, 1, angle)
maille.placerPapillon(premierPapillon)
premierPapillon.tracer()
courant = premierPapillon 
# Création de la première colonne :
i = 0
while i != maille.n -1:
    if (i%2) == 0:
        suivant = courant.ajouterPapillonInitColonne(courant.nm, courant.ne, pi/2.5)
    else :
        suivant = courant.ajouterPapillonInitColonne(courant.no, courant.nm, pi/2.5)
    maille.placerPapillon(suivant)
    suivant.tracer()
    courant = suivant    
    i = i + 1
    
# Création des autres papillons 
j = 1 # on a déjà tracé la première colonne donc on commence à 1
while (j < maille.m):
    # Papillon "du bas" - sur le bord
    courant = maille.get(0, j-1).ajouterPapillonHrzt(maille.get(1, j-1).se)
    courant.tracer()
    maille.placerPapillon(courant)
    i = 1
    # Papillons à l'intérieur
    while (i < maille.n):
        if (i%2) != 0:
            suivant = courant.ajouterPapillonVertSimple(maille.get(i, j-1)) 
        else:
            if i == maille.n - 1:
                suivant = courant.ajouterPapillonVertDernier(maille.get(i, j-1))
            else:
                suivant = courant.ajouterPapillonVert(maille.get(i, j-1), maille.get(i+1,j-1).se)
        suivant.tracer()
        maille.placerPapillon(suivant)
        courant = suivant      
        i = i + 1
    j = j + 1
    
plt.axis([0, 8, 0, 4])
plt.show() 

## transformation des mailles de papillons en liste de points
liste_pts = ListePoints(maille)
liste_pts.afficher()

plt.axis([0, 8, 0, 4])
plt.show()    