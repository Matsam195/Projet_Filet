# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 16:35:30 2017

@author: batim
"""

from math import *
from Point import *
from Papillon import *

origine = Point(0, 0, 0)
premierPapillon = Papillon(origine, 1, pi/(2.5))

origine.afficherPoint()
premierPapillon.tracer()
plt.axis([0, 5, 0, 5])
plt.show() 