from OpenGL.GL import *
from OpenGL.GLU import *
import sys
sys.path.append('C:/Users/samue/OneDrive/Desktop/NEAT/')
from Neural_Network import globalvars
import barrier

class Walls: 
    def __init__(self):
        self.back_wall_vertices = (
            (50, -10, -60),
            (0, -10, -60),
            (0, 20, -60),
            (50, 20, -60),
        )


        self.back_wall_surface = (
            (0, 1, 2, 3) 
        )
        
        self.floor_vertices = (
            (50, -10, -10),
            (0, -10, -10),
            (0, -10, -60),
            (50, -10, -60),   
        )

        self.floor_surface = (
            (0, 1, 2, 3)
        )
         
        self.target_surface = (
            (0, 1, 2, 3)
        )
        

    def Draw_Back_Wall(self):
        
        glBegin(GL_QUADS)
        
        for back_wall_vertex in self.back_wall_surface:
            glColor3fv((0, 0, 1))
            glVertex3fv(self.back_wall_vertices[back_wall_vertex])
        
        glEnd()
        
    def Draw_Target(self):
        
        glBegin(GL_QUADS) 
        
        for target_vertex in self.target_surface:
            glColor3fv((0, 1, 1))
            glVertex3fv(globalvars.globalvars.target_vertices[target_vertex])
        
        glEnd()
    
    def Draw_Floor(self):
    
        glBegin(GL_QUADS)

        for floor_vertex in self.floor_surface:
            glColor3fv((1, 0, 0))
            glVertex3fv(self.floor_vertices[floor_vertex])

        glEnd()