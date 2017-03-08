# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 16:35:30 2017

@author: batim
"""

from math import *
from Point import *
from Papillon import *

# TODO :  
# faire le tracé du papillon 7
#  utiliser la maille pour remplacer premier et p 
# éventuellement mettre un booleen pair ou  impair à la place des if

longueur = 5
angle = pi/2.5
origine = Point(0, 0, 0)
premierPapillon = Papillon(origine, 1, 1, angle)
premierPapillon.tracer()
p1 = premierPapillon
max = 0
p = True
premier = True
while (max < longueur):
        #parité dans la maille
    if (p):
        voisin = premierPapillon.ajouterPapillonInitColonne(premierPapillon.nm, premierPapillon.ne, pi/2.5)
    else :
        voisin = premierPapillon.ajouterPapillonInitColonne(premierPapillon.no, premierPapillon.nm, pi/2.5)
    if (premier) :
        p4 = voisin
    voisin.tracer()
    max = max +1 
    premierPapillon = voisin    
    p = not p
    premier = False
    
max = 0
while (max < longueur-1):
    voisin2 = p1.ajouterPapillonHrzt(p4.se)
    voisin2.tracer()
    max2 = 0
    premier = True
    while (max2 < longueur):
        v3 = voisin2.ajouterPapillonVert()
        v3.tracer()
        if premier :
            patate = v3
        max2 = max2 + 1
        premier = False
        voisin2 = v3
    p1 = voisin2
    p4 = patate
    max = max + 1
    
plt.axis([0, 5, 0, 5])
plt.show() 