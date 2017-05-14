# -*- coding: utf-8 -*-
"""
Created on Sat May 13 10:00:20 2017

@author: lehoan
"""

from optimisation import optimisation
from Point import *

#####################################################################
#                     EXEMPLES D'UTILISATION
    
# ---------------------------------------------------------------------   
# Exemple simple
# attendu : P1opt = (1/sqrt2, 1/sqrt2)
# bleus: voisins
# rouge: point initial
# jaune: point optimisé
    
P1=Point(1.0/sqrt(2.0)+0.3, 1.0/sqrt(2.0)+0.3, 0.0)
P1=Point(1.0/sqrt(2.0), 1.0/sqrt(2.0), 0.0)
P2=Point(0.0, 0.0, 0.0)
P3=Point(2.0/sqrt(2.0), 0.0, 0.0)
P4=Point(1.0/sqrt(2.0), 1.0+1.0/sqrt(2.0), 0.0)

l=1
a = pi/3
ecartx = 0.02
ecarty = 0.9
ponderations = [1, 0, 0]

# TRIANGLE EQUILATERAL
P1=Point(0.5+0.2, sqrt(3)/6+0.3, 0.0)
P2=Point(0.0, 0.0, 0.0)
P3=Point(0.5, sqrt(3)/2, 0.0)
P4=Point(1.0, 0.0, 0.0)
# CONFIGURATION PAPILLON
#P1=Point(sin(a)+ecartx, 0+ecarty, 0)
#P2=Point(0, cos(a), 0)
#P3=Point(sin(a), 1, 0)
#P4=Point(2*sin(a), cos(a), 0)

N1 = (P3.x-P1.x)*(P2.x-P1.x)+(P3.y-P1.y)*(P2.y-P1.y)+(P3.z-P1.z)*(P2.z-P1.z)
N2 = (P4.x-P1.x)*(P3.x-P1.x)+(P4.y-P1.y)*(P3.y-P1.y)+(P4.z-P1.z)*(P3.z-P1.z)
S2 = sqrt((P2.x-P1.x)**2+(P2.y-P1.y)**2+(P2.z-P1.z)**2)
S3 = sqrt((P3.x-P1.x)**2+(P3.y-P1.y)**2+(P3.z-P1.z)**2)
S4 = sqrt((P4.x-P1.x)**2+(P4.y-P1.y)**2+(P4.z-P1.z)**2)
a1 = acos(N1/(S2*S3))
a2 = acos(N2/(S3*S4))

print("")
print("Point initial :")
print("a1 :", a1-a, "| a2 :", a2-a, "| 2pi/3 :", a)
print("L1 :", P1.distance(P2)-l, "| L2 :", P1.distance(P3)-l, "| L3 :", P1.distance(P4)-l, "| L :", l)
print("")

newP1=optimisation(P1,P2,P3,P4, l=l, a=a, pond=ponderations, graph=False)

plt.plot([P2.x, P3.x, P4.x], [P2.y, P3.y, P4.y], 'bo')
plt.plot([P1.x], [P1.y], 'ro')

P1 = newP1

N1 = (P3.x-P1.x)*(P2.x-P1.x)+(P3.y-P1.y)*(P2.y-P1.y)+(P3.z-P1.z)*(P2.z-P1.z)
N2 = (P4.x-P1.x)*(P3.x-P1.x)+(P4.y-P1.y)*(P3.y-P1.y)+(P4.z-P1.z)*(P3.z-P1.z)
S2 = sqrt((P2.x-P1.x)**2+(P2.y-P1.y)**2+(P2.z-P1.z)**2)
S3 = sqrt((P3.x-P1.x)**2+(P3.y-P1.y)**2+(P3.z-P1.z)**2)
S4 = sqrt((P4.x-P1.x)**2+(P4.y-P1.y)**2+(P4.z-P1.z)**2)
a1 = acos(N1/(S2*S3))
a2 = acos(N2/(S3*S4))

print("")
print("Point final :")
print("a1-a :", a1-a, "| a2-a :", a2-a, "| 2pi/3 :", a)
print("L1-L :", P1.distance(P2)-l, "| L2-L :", P1.distance(P3)-l, "| L3-L :", P1.distance(P4)-l, "| L :", l)
print("")

plt.plot([newP1.x], [newP1.y], 'yo')
plt.axis('equal')
plt.show()

print("")
print("Point attendu :")
print("a1-a :", a1-a, "| a2-a :", a2-a, "| 2pi/3 :", a)
print("L1-L :", P1.distance(P2)-l, "| L2-L :", P1.distance(P3)-l, "| L3-L :", P1.distance(P4)-l, "| L :", l)
print("")

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
# Exemple pour tester l'ajout du point miroir dans le calcul de l'énergie
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
       