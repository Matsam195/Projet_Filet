# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 16:05:12 2017

@author: belotm
"""

from ListePoints import *
from optimisation import *

# Conditions de stabilité
lastEnergie = 0
seuil = 0.01

def angleMax(maille):
    maximum = 0
    for i in range(1, maille.n-1):
        for j in range(1, maille.m-1):
            point = maille.get(i,j)
            voisins = maille.getVoisins(i, j)

            P1 = point
            P2 = voisins[0]
            P3 = voisins[1]
            P4 = voisins[2]
            N1 = (P3.x-P1.x)*(P2.x-P1.x)+(P3.y-P1.y)*(P2.y-P1.y)+(P3.z-P1.z)*(P2.z-P1.z)
            N2 = (P4.x-P1.x)*(P3.x-P1.x)+(P4.y-P1.y)*(P3.y-P1.y)+(P4.z-P1.z)*(P3.z-P1.z)
            S2 = sqrt((P2.x-P1.x)**2+(P2.y-P1.y)**2+(P2.z-P1.z)**2)
            S3 = sqrt((P3.x-P1.x)**2+(P3.y-P1.y)**2+(P3.z-P1.z)**2)
            S4 = sqrt((P4.x-P1.x)**2+(P4.y-P1.y)**2+(P4.z-P1.z)**2)
            a1 = acos(N1/(S2*S3))
            a2 = acos(N2/(S3*S4))
            
            if (a1 > maximum):
                maximum = a1
            if (a2 > maximum):
                maximum = a2
            
    return maximum

def energieMaille(maille, longueur, e, angle, ponderations):
    """
    Evalue l'énergie totale de la maille, selon le critères d'énergie longueur, e, angle et ponderations (cf. help(Energie))
    """
    somme = 0
    for i in range(1, maille.n-1):
        for j in range(1, maille.m-1):
            point = maille.get(i,j)
            voisins = maille.getVoisins(i, j)
            somme += Energie(point, voisins[0], voisins[1], voisins[2], voisins[3], longueur, e, angle, ponderations)
    return somme

def energieAssezFaible(point, voisins, longueur, e, angle, ponderations):
    return(Energie(point, voisins[0], voisins[1], voisins[2], voisins[3], longueur, e, angle, ponderations) < seuil)


def estStable1(maille, longueur, e, angle, ponderations):
    """
    Estime si la maille est stable, selon les critères d'énergie longueur, e, angle et ponderations (cf. help(Energie)).
    Méthode 1 : si un point de la maille a plus d'énergie que le seuil, la maille n'est pas stable.
                si tous les points de la maille ont moins d'énergie que le seuil, la maille est stable.
    """
    maximum = 0
    for i in range(1, maille.n_pap-1):
        for j in range(1, maille.m_pap-1):
            point = maille.get(i,j)
            voisins = maille.getVoisins(i, j)
            if (not energieAssezFaible(point, voisins, longueur, e, angle, ponderations)):
                return False
    return True

def estStable2(maille, longueur, e, angle, ponderations):
    """
    Estime si la maille est stable, selon les critères d'énergie longueur, e, angle et ponderations (cf. help(Energie)).
    Méthode 2 : si l'optimisation a fait varier l'énergie totale de la maille d'au moins seuil, la maille n'est pas stable.
                si la variation de l'énergie totale de la maille est inférieure au seuil, la maille est stable.
    """
    global lastEnergie
    energie = energieMaille(maille, longueur, e, angle, ponderations)
    stable = abs(energie-lastEnergie) < seuil
    lastEnergie = energie
    return stable
