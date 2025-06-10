import sys
sys.path.append('C:/Users/samue/OneDrive/Desktop/NEAT/')
from Neural_Network import globalvars
import random
import keyboard
from Cube import Cube
import math
 
class Player(Cube):  
    def __init__(self, brain):
        super().__init__()
        self.gen = 0
        self.fitness = 0 
        self.x_center= sum(vertex[0] for vertex in globalvars.globalvars.target_vertices) / len(globalvars.globalvars.target_vertices)
        self.y_center = sum(vertex[1] for vertex in globalvars.globalvars.target_vertices) / len(globalvars.globalvars.target_vertices)
        self.z_center = sum(vertex[2] for vertex in globalvars.globalvars.target_vertices) / len(globalvars.globalvars.target_vertices)
        
        self.brain = brain
    
    def update(self, move=None):
        self.update_target()

        if move is None:
            outputs = self.brain.fast_run([
                self.cube_pos[0],
                self.cube_pos[1],
                self.cube_pos[2],
                math.sin(math.radians(self.direction)),
                math.cos(math.radians(self.direction)),
                self.x_center,
                self.z_center,
            ])

            actions = []
            if outputs[0] > 0.75:
                actions.append("w")
            if outputs[1] > 0.75:
                actions.append("d")
            if outputs[2] > 0.75:
                actions.append("a")
            if outputs[3] > 0.75:
                actions.append("u")

            move = "".join(actions)

        self.move(move)

            
        self.distance_from_target = ((self.x_center - self.cube_pos[0]) ** 2 + 
                            (self.y_center - self.cube_pos[1]) ** 2 + 
                            (self.z_center - self.cube_pos[2]) ** 2) ** 0.5 
        self.fitness += self.distance_from_target
        
    def update_target(self):
        self.x_center = (globalvars.globalvars.target_vertices[0][0] + globalvars.globalvars.target_vertices[1][0])/2
        self.y_center = -9.5
        self.z_center = (globalvars.globalvars.target_vertices[0][2] + globalvars.globalvars.target_vertices[2][2])/2
 
 #deprecated function           
        
    def collide_with_target(self):
        corner1 = (self.cube_pos[0] + 1, self.cube_pos[2] - 1)
        corner2 = (self.cube_pos[0] + 1, self.cube_pos[2] + 1)
        corner3 = (self.cube_pos[0] - 1, self.cube_pos[2] + 1)
        corner4 = (self.cube_pos[0] - 1, self.cube_pos[2] - 1)
         
        targetxrange = (self.x_center + 2.5, self.x_center - 0.5)
        targetzrange = (self.z_center + 2.5, self.z_center - 2.5)
        
        if (targetxrange[0] > corner1[0] > targetxrange[1]) and (targetzrange[0] > corner1[1] > targetzrange[1]):
            return True
        elif (targetxrange[0] > corner2[0] > targetxrange[1]) and (targetzrange[0] > corner2[1] > targetzrange[1]):
            return True
        elif (targetxrange[0] > corner3[0] > targetxrange[1]) and (targetzrange[0] > corner3[1] > targetzrange[1]):
            return True
        elif (targetxrange[0] > corner4[0] > targetxrange[1]) and (targetzrange[0] > corner4[1] > targetzrange[1]):
            return True
        else:
            return False
 
    def crossover(self, other_player):
        child = self.__class__()
        child.brain = self.brain.crossover(other_player.brain)
        return child

    
    
    