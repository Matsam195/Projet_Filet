# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 14:57:07 2017

@author: batim
"""

from Point import *

class Papillon:
    """Un papillon regroupe 6 points nommés par leur 'position géographique' """
        
    def __init__(self):
        self.so = Point()
        self.no = Point()
        self.nm = Point()
        self.ne = Point()
        self.sm = Point()
        self.se = Point()

        
    def __init__(self, p1, lh, lv, angle):
        """création du premier papillon
            lv : longueur du coté vertical d'un papillon
            lh : idem en horizontal 
            angle : permet de créer un papillon parfait, pi/3 <= angla <= pi/2"""   
        #assert(pi/3 <= angle)
        #assert(angle <= pi/2)
        #assert(lh <= lv/2 /cos(angle))
        self.so = p1        
        self.no = Point(self.so.x, self.so.y + lv, 0) 
        self.nm = Point(sin(angle)*lh + self.no.x, -cos(angle)*lv + self.no.y, 0)
        self.ne = Point(sin(angle)*lh + self.nm.x, self.no.y, 0)
        self.sm = Point(self.so.x + sin(angle)*lh, cos(angle)*lv + self.so.y, 0)
        self.se = Point(self.so.x + 2*sin(angle)*lh, self.so.y, 0)  

  
    def ajouterPapillonInitColonne(self, p1, p2, angle):
        """Création du papillon voisin de celui en paramètre
            les longueurs du papillon sont celles de [p1, p2]"""    
        longueur = p1.distance(p2)
            
        if self.nm == p1 and self.ne == p2:
            so = p1
            voisin = Papillon(so, longueur, longueur, angle)
            voisin.so.libre = False
            voisin.sm.libre = False
            
        elif self.no == p1 and self.nm == p2:
            so = Point(p2.x - 2*sin(angle)*longueur, p2.y, 0)  
            voisin = Papillon(so, longueur, longueur, angle)
            voisin.se.libre = False
            voisin.sm.libre = False
            
        else:
            print("ERREUR !, tentative de créer un papillon à partir de points incohérents ")
            return 
        return voisin
            
            
    def ajouterPapillonHrzt(self, p3):
        """Ajoute un papillon à droite à partir d'un point nm voisin
            on vérifie que le papillon aura un géométrie 'normale' """        
        print(p3.x)
        print(p3.y)
        lvert = self.ne.distance(self.se)
        lhrzt = self.ne.distance(p3)
        angle = acos((self.se.distance(p3)**2 - lhrzt**2 - lvert**2) / (-2*lhrzt*lvert))     

        #assert(lhrzt <= lvert/2 /cos(angle))
        print(self.se.x)
        print(self.se.y)
        voisin = Papillon(self.se, lhrzt, lvert, angle)
        voisin.no.libre = False
        voisin.so.libre = False
        voisin.nm.libre = False
        return voisin
        
        
    def ajouterPapillonVertSimple(self, voisH):
        # Ajout d'un papillon vertical :
        #assert(voisH.se == self.nm) 
        # Cas du voisin vertical le plus libre 
        # seuls trois points sont fixés
        lvert = self.nm.distance(self.no)
        lhrzt = self.so.distance(self.sm)
        angle = abs(acos((self.sm.distance(self.no)**2 - lhrzt**2 - lvert**2) / (-2*lhrzt*lvert)))     

        voisin = Papillon(self.nm, lhrzt, lvert, angle)
        return voisin
        
        
        # on construit le voisin le moins libre : 1 seul point ne à choisir
        # on le construit par symétrie avec la partie collée au papillon dessous
    def ajouterPapillonVert(self, voisH, se):
        pap = Papillon(Point(0,0,0), 0, 0, 0)
        pap.so = voisH.se
        pap.no = voisH.ne
        pap.nm = se
        dy = self.no.y - self.nm.y  
        pap.ne = Point(self.nm.x, se.y+dy, 0)
        pap.se = self.nm
        pap.sm = self.no
        #lh = self.no.distance(nm)
        return pap
                        
    def ajouterPapillonVertDernier(self, voisH):
        dy = voisH.se.y - self.ne.y 
        return self.ajouterPapillonVert(voisH, Point(self.no.x, voisH.ne.y + dy, 0)) 
        
        
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
        













