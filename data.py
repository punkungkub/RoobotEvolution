import matplotlib.pyplot as plt
import numpy as np
import pickle, json
import os,shutil
from threading import Thread

class data:
    def __init__(self):
        self.generation=[]
        self.fitness={}
        self.data={}
        
    def storage(self, gen, data):
        self.generation.append(gen)
        self.data.update({gen:data})
        fitness,data=[],[]
        for person in data:
            fitness.append(data[person]['fitness'])
        self.fitness[gen]=fitness
            
    def plot(self):
        plt.figure()
        for x in self.fitness:
            for y in self.fitness[x]:
                plt.scatter(x, y,c='k')
        plt.savefig('dot_plot.jpeg')
        
    def saveData(self):
        with open('data.txt', 'w') as outfile:
            json.dump(self.fitness, outfile, indent=4)
    
    def saveProperty(self):
        with open('current_robot.txt', 'w') as outfile:
            json.dump(self.data, outfile, indent=4)
    
    def moveData(self):
        print("Backing up data ...")
        path=os.path.join(os.getcwd(),'dataStorage')
        if not os.path.exists(path):
            os.mkdir(path)
        else:
            return
        shutil.move(os.path.join(os.getcwd(),'dot_plot.jpeg'),os.path.join(path,'dot_plot.jpeg'))
        shutil.move(os.path.join(os.getcwd(),'data.txt'),os.path.join(path,'data.txt'))
        shutil.move(os.path.join(os.getcwd(),'current_robot.txt'),os.path.join(path,'current_robot.txt'))
        print("Completed!")
        