#!/usr/bin/python3

from environment import *
from robot import *
from calculation import *
from evolution import *
from data import *
from vpython import * 

import numpy as np
import os,sys
import warnings
warnings.filterwarnings("ignore")

if os.path.exists(os.path.join(os.getcwd(),'dataStorage')):
    print('Data Existed!!!')
    sys.exit()
    
generation = 100
century =100
population = 50
init_pos=[0,0,0]
nMass=6
edge_length=1

def init_sphere():
    population_info={}
    for people in range(population):
        robot_sim=robot(init_pos=init_pos,nMass=nMass,edge=edge_length)
        mass=robot_sim.cube()
        population_info.update({people:{'sphere':robot_sim.genSphere(mass),'fitness':0}})
    return population_info

material = [[1000, 0, 2*pi, 0],
            [20000, 0, 2*pi, 0],
            [5000, 1e-3, 2*pi, 0],
            [5000, 1e-3, 2*pi, pi]]

# environment = environment(2)
# environment.checkerBoard(10)
population_info=init_sphere()
past_population=population_info
data_management=data()

for decade in range(1,century):
    for gen in range(1,generation):
        print('Generation: {}'.format(gen*decade))
        past_population=population_info
        digiEvol = evolution(population=population_info)
        digiEvol.mutation_size()
        digiEvol.mutation_center()
        population_info=digiEvol.crossover()
        for people in population_info:
            print('Robot: {}'.format(people+1))
            robot_sim=robot(init_pos=init_pos,nMass=nMass,edge=edge_length)
            mass=robot_sim.cube()
            spring=robot_sim.genSpring(spherePos=population_info[people]['sphere'])
            # robot_sim.showBalls(spherePos=population_info[people]['sphere'])
            calculate=calculation(mass=mass,spring=spring,material=material)
            # calculate.init_anime()
            calculate.sim(time=3,delta=0.001)
            # calculate.invisible()
            inst_fitness=calculate.fitness()
            if inst_fitness > population_info[people]['fitness']:
                population_info.update({people:{'sphere':population_info[people]['sphere'],'fitness':calculate.fitness()}})
            else:
                population_info.update({people:past_population[people]})
            calculate=0
            robot_sim=0
        
        population_info=digiEvol.selection()
        digiEvol=0
        data_management.storage(gen=gen*decade, data=population_info)
        data_management.saveData()
        data_management.saveProperty()
        data_management.plot()
    data_management.moveData()
