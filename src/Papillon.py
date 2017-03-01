# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 14:57:07 2017

@author: batim
"""

from Point import *

class Papillon:
    """Un papillon regroupe 6 points"""
        
    
    
    def __init__(self, p1, l, angle):
        """création du premier papillon"""   
        self.so = p1        
        self.no = Point(self.so.x, self.so.y + l, 0) 
        self.nm = Point(sin(angle)*l + self.no.x, -cos(angle)*l + self.no.y, 0)
        self.ne = Point(sin(angle)*l + self.nm.x, self.no.y, 0)
        self.sm = Point(self.so.x + sin(angle)*l, cos(angle)*l + self.so.y, 0)
        self.se = Point(self.so.x + 2*sin(angle)*l, self.so.y, 0)
  
            
    def tracer(self):
        self.no.afficherPoint()    
        self.nm.afficherPoint()    
        self.ne.afficherPoint()    
        self.so.afficherPoint()    
        self.sm.afficherPoint()    
        self.se.afficherPoint()        
        
        self.so.afficherSegment(self.no)
        self.no.afficherSegment(self.nm)
        self.nm.afficherSegment(self.ne)
        self.ne.afficherSegment(self.se)
        self.se.afficherSegment(self.sm)
        self.sm.afficherSegment(self.so)
        
