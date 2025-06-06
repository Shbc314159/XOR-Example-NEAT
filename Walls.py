from OpenGL.GL import *
from OpenGL.GLU import *
import sys
sys.path.append('C:/Users/samue/OneDrive/Desktop/NEAT/')
from Neural_Network import globalvars

class Walls: 
    def __init__(self):
        self.back_wall_vertices = globalvars.globalvars.back_wall_vertices
        self.back_wall_surface = globalvars.globalvars.back_wall_surface
        
        self.floor_vertices = globalvars.globalvars.floor_vertices
        self.floor_surface = globalvars.globalvars.floor_surface
         
        self.target_surface = globalvars.globalvars.target_surface
        

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