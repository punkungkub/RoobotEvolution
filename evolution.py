from random import *
from robot import robot
import numpy as np

class evolution:
    def __init__(self, population):
        # super().__init__(init_pos, nMass, edge)
        self.population=population
        # self.mass = self.cube()
        # self.tmp = max(self.massArr[:,2]),max(self.massArr[:,3]),max(self.massArr[:,4])
        
    def mutation_size(self):
        prob=random()
        num_mutate=round(len(self.population)*prob)
        population_mutate=sample(list(self.population),num_mutate)
        for person in population_mutate:
            for indx,sphere in enumerate(self.population[person]['sphere']):
                toss=random()
                if toss >= 0.7:
                    self.population[person]['sphere'][indx]['radius']=sphere['radius']+random() 
                elif toss >= 0.3:
                    self.population[person]['sphere'][indx]['radius']=sphere['radius']-random()
                else:
                    pass
            
    def mutation_center(self):
        prob=random()
        num_mutate=round(len(self.population)*prob)
        population_mutate=sample(list(self.population),num_mutate)
        for person in population_mutate:
            for indx,sphere in enumerate(self.population[person]['sphere']):
                toss=random()
                if toss >= 0.7:
                    self.population[person]['sphere'][indx]['center']=list(np.array(sphere['center'])+random()) 
                elif toss >= 0.3:
                    self.population[person]['sphere'][indx]['center']=list(np.array(sphere['center'])-random())
                else:
                    pass
    
    def crossover(self):
        order = sorted(self.population, key=lambda x: self.population[x]['fitness'], reverse=True)
        child_A={}
        child_B={}
        for indx in range(0,len(self.population),2):
            choose = randint(1,3)
            unChoose = 4-choose
            parent_A=[]
            parent_B=[]
            for ind in range(choose):
                parent_A.append(self.population[order[indx]]['sphere'][ind])
                parent_B.append(self.population[order[indx+1]]['sphere'][ind])
            for ind in range(unChoose):
                parent_A.append(self.population[order[indx+1]]['sphere'][ind])
                parent_B.append(self.population[order[indx]]['sphere'][ind])
            child_A[max(order)+indx+1] = {'sphere':parent_A, 'fitness':0}
            child_B[max(order)+indx+2] = {'sphere':parent_B, 'fitness':0}
        
        self.population.update(child_A)
        self.population.update(child_B)
        return self.population
        
    def selection(self):
        rank = sorted(self.population, key=lambda x: self.population[x]['fitness'])
        for k in range(int(len(rank)/2)):
            self.population.pop(rank[k])
        return self.population