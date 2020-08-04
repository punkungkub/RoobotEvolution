
from vpython import *

class environment:
    def __init__(self, size):
        self.checkerSize = size

    def checkerBoard(self, dim):
        dim*=self.checkerSize
        for j in range(-dim,dim):
            for k in range(-dim,dim):
                pos = vector(k*self.checkerSize,-0.25,j*self.checkerSize)
                size = vector(self.checkerSize,0.5,self.checkerSize)
                if (k+j)%2 == 0:
                    floor = box(pos=pos,size=size,color=color.white)
                else:
                    floor = box(pos=pos,size=size,color=color.gray(0.5))
    