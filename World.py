import sys
sys.path.append('C:/Users/samue/OneDrive/Desktop/NEAT/')
from Neural_Network import globalvars
from Player import *
from Walls import *
import pygame
import pygame
from pygame.locals import *
import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

from OpenGL.GL import *
from OpenGL.GLU import *
import barrier

class World():
    def __init__(self):
        if not pygame.get_init():
            pygame.init()
        display = (1600,1000)
        pygame.display.gl_set_attribute(GL_MULTISAMPLESAMPLES, 10)
        pygame.display.set_mode(display, DOUBLEBUF|OPENGL|RESIZABLE)

        gluPerspective(45, (display[0]/display[1]), 0.1, 110.0)
        glTranslatef(-50, -5, -20)
        glRotatef(25, 2, 0, 0)
        glEnable(GL_DEPTH_TEST)

        self.walls = Walls()

    def draw(self, player):
        # maintain backward compatibility for drawing a single player
        self.draw_multi([player])

    def draw_multi(self, players):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glClearColor(0, 0, 0, 1)

        self.walls.Draw_Back_Wall()
        self.walls.Draw_Floor()
        self.walls.Draw_Target()

        for barrier in globalvars.globalvars.barriers:
            barrier.draw()

        for p in players:
            p.draw()

        pygame.display.flip()
    @classmethod
    def randomise_target(self):
        """
        x = random.randint(0, 45)
        z = random.randint(-50, -15)
        """
        z = globalvars.globalvars.z
        if globalvars.globalvars.x == 25:
            x = 70
        elif globalvars.globalvars.x == 70:
            x = 25
        else:
            x = 25
        
        
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