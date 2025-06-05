import sys
sys.path.append('C:/Users/samue/OneDrive/Desktop/NEAT/')
from Neural_Network import globalvars
from Player import *
from Walls import *
import pygame
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

class World():
    def __init__(self):
        pygame.init()
        display = (1600,1000)
        pygame.display.gl_set_attribute(GL_MULTISAMPLESAMPLES, 10)
        pygame.display.set_mode(display, DOUBLEBUF|OPENGL|RESIZABLE)

        gluPerspective(45, (display[0]/display[1]), 0.1, 110.0)
        glTranslatef(0, -5, -20)
        glRotatef(25, 2, 0, 0)
        glEnable(GL_DEPTH_TEST)

        self.walls = Walls()

    def draw(self, player):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glClearColor(0, 0, 0, 1)

        self.walls.Draw_Back_Wall()
        self.walls.Draw_Floor()
        self.walls.Draw_Target()
        
        for barrier in globalvars.globalvars.barriers:
            barrier.draw()
        
        player.draw()
        
        pygame.display.flip()
    @classmethod
    def randomise_target(self):
        """
        x = random.randint(0, 45)
        z = random.randint(-50, -15)
        """

        x = -22
        z = -15
        if globalvars.globalvars.x == 22:
            x = -22
        elif globalvars.globalvars.x == -22:
            x = 22
        
        
        globalvars.globalvars.set_target_vertices(x, z)
        
        
    def randomise_barriers(self):
        globalvars.barriers = []
        globalvars.barriers_vertices = []
        
        for i in range(0):
            length = random.randint(2, 10)
            height = random.randint(2, 15)
            width = random.randint(2, 10)
            xmin = random.randint(-25, 15)
            ymin = -10
            zmin = random.randint(-60, -20)
            xmax = xmin + length
            ymax = ymin + height
            zmax = zmin + width
            newbarrier = barrier.Barrier(xmin, xmax, ymin, ymax, zmin, zmax)
            globalvars.barriers.append(newbarrier)
            globalvars.barriers_vertices.append(newbarrier.vertices)