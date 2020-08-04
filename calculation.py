import numpy as np
from math import *
from vpython import *

class calculation:
    def __init__(self, mass, spring, material):
        self.massArr = mass
        self.springArr = spring
        
        self.kground=1e4
        self.g=-9.81 #gravity in m/s^2
        self.us = 0.99
        self.uk = 0.8
        self.damping=0.999
        self.t=0
        
        self.material = material
        
        self.animateMS={}
        
    def Forces(self):
        mF = np.zeros((len(self.massArr),3))
        for ind,spring in enumerate(self.springArr):
            
            k,a,b,c=self.material[spring[0]]
            new_spring=self.Breath(spring=spring,a=a,b=b,c=c)
            self.springArr[ind]=spring
            
            deltaSpring = np.array(self.massArr[spring[3]][1:4])-np.array(self.massArr[spring[2]][1:4])
            LfSp = np.linalg.norm(deltaSpring)
            unitVector=deltaSpring/LfSp
            sF = -k*(spring[1]-LfSp)
            
            fx = sF*unitVector[0]
            fy = sF*unitVector[1]
            fz = sF*unitVector[2]
            
            mF[spring[2]][0] += fx
            mF[spring[2]][1] += fy
            mF[spring[2]][2] += fz
            mF[spring[3]][0] += -fx
            mF[spring[3]][1] += -fy
            mF[spring[3]][2] += -fz
        self.massArr[:,7:10]=mF
        self.Friction()
        
    def Kinematics(self, delta):
        self.Forces()
        for ind, mass in enumerate(self.massArr):
            # acceleration
            mass[8] += self.g*mass[0] if mass[2]>0 else self.g*mass[0]-self.kground*mass[2]
            self.ForcetoAcc(mass)
            # velocity
            mass[6] += mass[9]*delta
            mass[5] += mass[8]*delta
            mass[4] += mass[7]*delta
            mass = self.damp(mass)
            # position
            mass[3] += mass[6]*delta
            mass[2] += mass[5]*delta
            mass[1] += mass[4]*delta
            self.massArr[ind]=mass
            
    def Friction(self):
        for ind,mass in enumerate(self.massArr):
            fH=np.linalg.norm([mass[9],mass[7]])
            unit_vector=np.array([mass[9],mass[7]])/fH
            friction=0 if mass[2]>0 else -self.us*(self.g*mass[0]+self.kground*mass[2])
            if -self.kground*mass[2] >0:
                if fH<friction:
                    fz,fx = 0,0
                else:
                    new_fH=fH-self.uk*self.g*mass[0]
                # unit vector
                    fz,fx=unit_vector*new_fH
            
                self.massArr[ind,9]=fz
                self.massArr[ind,7]=fx
            # print(fz,fx,new_fH)
                   
    def damp(self, mass):
        mass[4]*=self.damping
        mass[5]*=self.damping
        mass[6]*=self.damping
        return mass
        
    def ForcetoAcc(self, mass):
        mass[9]/=mass[0]
        mass[8]/=mass[0]
        mass[7]/=mass[0]
    
    def Breath(self,spring,a,b,c):
        spring[1]+=a*sin(b*self.t+c)
        return spring
        
    def fitness(self):
        return np.linalg.norm([(max(self.massArr[:,7])+min(self.massArr[:,7]))/2,
                               (max(self.massArr[:,9])+min(self.massArr[:,9]))/2])
        
    def init_anime(self):
        ballarray,springsarray=[],[]
        c=[vector(0,0,1),vector(0,1,0),vector(1,0,0),vector(0.5,0.5,0.5)]
        # for mass in self.massArr:
        #     pos = vector(mass[1],mass[2],mass[3])
        #     ball = sphere(pos=pos, radius=0.15, color=color.yellow)
        #     ballarray.append(ball)
        for spring in self.springArr:
            pos = vector(self.massArr[spring[2]][1],self.massArr[spring[2]][2],self.massArr[spring[2]][3])
            axis = np.array(self.massArr[spring[3]])-np.array(self.massArr[spring[2]])
            axis = vector(axis[1],axis[2],axis[3])
            sp = cylinder(pos=pos, axis=axis, radius=0.05, color=c[spring[0]])
            springsarray.append(sp)
        self.animateMS={'mass':ballarray, 'spring':springsarray}
    
    def animate(self):
        # for ind,ball in enumerate(self.animateMS['mass']):
        #     mass = self.massArr[ind]
        #     ball.pos = vector(mass[1],mass[2],mass[3])
        springObj=self.animateMS['spring']
        for ind,spring in enumerate(self.springArr):
            axis = np.array(self.massArr[spring[3]])-np.array(self.massArr[spring[2]])
            axis = vector(axis[1],axis[2],axis[3])
            mass = self.massArr[spring[2]]
            springObj[ind].pos=vector(mass[1],mass[2],mass[3])
            springObj[ind].axis=axis
            
    def sim(self, time, delta):
        while self.t<=time:
            for tmp in range(0,100):
                self.Kinematics(delta)
                self.t+=delta
            # self.animate()
            
    def invisible(self):
        for ind,ball in enumerate(self.animateMS['mass']):
            ball.visible=False
        springObj=self.animateMS['spring']
        for ind,spring in enumerate(self.springArr):
            springObj[ind].visible=False