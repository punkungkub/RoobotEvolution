
import numpy as np
from random import choice, uniform
from math import *
from vpython import *

class robot:
    def __init__(self, init_pos, nMass, edge):
        
        self.x=init_pos[0]
        self.y=init_pos[1]
        self.z=init_pos[2]
        
        self.mass = 0.1 #mass in kg 
        self.vertices = []
        self.spring=[]
        self.massArr=[]
        self.edge = edge
        self.dimRobot = nMass*self.edge
        self.offset=4
        self.animateMS={}
    
    def cube(self):
        for z in range(0,self.dimRobot, self.edge):
            for y in range(0, self.dimRobot, self.edge):
                for x in range(0,self.dimRobot, self.edge):
                    self.vertices.append([float(x),float(y),float(z)])
        self.massArr = np.array(list([self.mass,vertex[0],vertex[1]+self.y,vertex[2], 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] for vertex in self.vertices))
        return self.massArr
    
    def genSpring(self, spherePos):
        posMass = len(self.vertices)
        for spring in range(posMass):
            for nextSpring in range(posMass):
                restLength = np.linalg.norm(np.array(self.vertices[spring])-np.array(self.vertices[nextSpring]))
                midPoint=(np.array(self.massArr[spring][1:4])+np.array(self.massArr[nextSpring][1:4]))/2
                if restLength >= self.edge*2:
                    pass
                elif spring==nextSpring:
                    pass
                else:
                    indencode=self.detK(midPoint=midPoint,spherePos=spherePos)
                    if spring < nextSpring:
                        self.spring.append([indencode, restLength, spring, nextSpring])
                    else:
                        self.spring.append([indencode, restLength, nextSpring, spring])
        
        tmp=set()
        for sp in self.spring:
            tmp.add(tuple(sp))
        self.spring=[list(x) for x in tmp]
        return self.spring
    
    def detK(self,midPoint,spherePos):
        tmp={}
        for indx,k in enumerate(spherePos):
            if np.linalg.norm(midPoint-k['center']) <= k['radius']:
                tmp.update({np.linalg.norm(midPoint-k['center']):indx})
        mat = tmp[min(tmp.keys())] if tmp else 3
        return mat
    
    def showBalls(self,spherePos):
        c=[vector(0,0,1),vector(0,1,0),vector(1,0,0),vector(0.5,0.5,0.5)]
        for idx,point in enumerate(spherePos):
            x,y,z=point['center']
            center=vector(x,y,z)
            ball=sphere(pos=center, radius=point['radius'], color=c[idx], opacity =0.8)
        
    def genSphere(self,mass):
        centerRadius=[]
        tmp=[max(mass[:,2]),max(mass[:,3]),max(mass[:,4])]
        for _ in range(4):
            centerRadius.append({'center':[uniform(min(mass[:,1])-self.offset,max(mass[:,1])+self.offset),
                                 uniform(min(mass[:,2])-self.offset,max(mass[:,2])+self.offset),
                                 uniform(min(mass[:,3])-self.offset,max(mass[:,3])+self.offset)],
                                 'radius':uniform(self.offset,sum(tmp)/len(tmp))*1.5})
        return centerRadius

                