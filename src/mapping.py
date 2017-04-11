import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

from math import *
from Papillon import *
from Point import *

mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = fig.gca(projection='3d')

#x=[0,1,2,2,1,0,0]
#y=[0,1,0,3,2,3,0]
#z=[0,0,0,0,0,0,0]
#
#ax.plot(x, y, z, label='PAPILLON')
#
#x=[0,1,2,2,1,0,0]
#y=[0,1,0,3,2,3,0]
#z=[1,1,1,1,1,1,1]
#ax.plot(x, y, z, label='salut')
#ax.legend()



#prendre en compte et tracer point et voisins
def placerPointsSurf(listePoints, Surface):
   for papillon in listePoints:
        current = papillon.no
        papillon.no = Point(current.x, current.y, sin(current.x))
        current = papillon.so
        papillon.so = Point(current.x, current.y, sin(current.x))
        current = papillon.nm
        papillon.nm = Point(current.x, current.y, sin(current.x))
        current = papillon.ne
        papillon.ne = Point(current.x, current.y, sin(current.x))
        current = papillon.sm
        papillon.sm = Point(current.x, current.y, sin(current.x))
        current = papillon.se
        papillon.se = Point(current.x, current.y, sin(current.x))
        
        x = [papillon.so.x, papillon.no.x, papillon.nm.x, papillon.ne.x, papillon.se.x, papillon.sm.x, papillon.so.x]
        y = [papillon.so.y, papillon.no.y, papillon.nm.y, papillon.ne.y, papillon.se.y, papillon.sm.y, papillon.so.y]
        z = [papillon.so.z, papillon.no.z, papillon.nm.z, papillon.ne.z, papillon.se.z, papillon.sm.z, papillon.so.z]
        ax.plot(x, y, z)
        
        
liste = [Papillon(Point(0,0,0), 5, pi/2.5)]
placerPointsSurf(liste, 0)
plt.show()