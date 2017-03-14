# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 12:01:39 2017

@author: batim
"""

from math import *
from Point import *
from Papillon import *

# TODO :  
# faire le tracé du papillon 7
# utiliser la maille pour remplacer premier et p 
# éventuellement mettre un booleen pair ou  impair à la place des if

angle = pi/2.5

maille = Maille(6,3)

# Création de l'origine - 1er papillon en (0,0)
origine = Point(0, 0, 0)
premierPapillon = Papillon(origine, 1, 1, angle)
maille.placerPapillon(0, 0, premierPapillon)
premierPapillon.tracer()
courant = premierPapillon 
# Création de la première colonne :
i = 0
while i != maille.n:
    if (i%2) == 0:
        suivant = courant.ajouterPapillonInitColonne(courant.nm, courant.ne, pi/2.5)
    else :
        suivant = courant.ajouterPapillonInitColonne(courant.no, courabnt.nm, pi/2.5)
    suivant.tracer()
    courant = suivant    
    i = i + 1
    
# Création des autres papillons 
i = 1 # on a déjà tracé la première colonne donc on commence à 1
while (i < maille.n-1):
    # Papillon "du bas" - sur le bord
    courant = maille[i-1,0].ajouterPapillonHrzt(maille[i-1, 0].se)
    courant.tracer()
    j = 0
    # 
    while (j < maille.m):
        suivant = courant.ajouterPapillonVert()
        suivant.tracer()
        courant = suivant        
    i = i + 1
    
plt.axis([0, 5, 0, 5])
plt.show() 