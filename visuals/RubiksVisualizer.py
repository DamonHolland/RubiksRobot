from threading import Thread

import pygame
import numpy as np
from model.RubiksCube import RubiksCube
from pygame.locals import *
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *

ColorDict = {RubiksCube.WHITE: (1, 1, 1),
             RubiksCube.GREEN: (0, 1, 0),
             RubiksCube.RED: (1, 0, 0),
             RubiksCube.BLUE: (0, 0, 1),
             RubiksCube.ORANGE: (1, 0.5, 0),
             RubiksCube.YELLOW: (1, 1, 0)}
BLACK = (0, 0, 0)


class RubiksVisualizer:
    WINDOW_HEIGHT = 720
    WINDOW_WIDTH = 720
    ROTATE_SPEED = 0.005
    x_angle = 0
    y_angle = 0
    z_angle = 0

    def __init__(self, rubiks_cube):
        Thread(target=self.start, args=[rubiks_cube]).start()


    def start(self, rubiks_cube):
        pygame.init()
        pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), DOUBLEBUF | OPENGL)
        gluPerspective(45, self.WINDOW_WIDTH / self.WINDOW_HEIGHT, 0.1, 50.0)
        glEnable(GL_DEPTH_TEST)
        glTranslatef(0.0, 0.0, -8)
        pygame.display.set_caption("Rubik's Cube")
        running = True
        drag = False
        prev_mouse_pos = [0, 0]
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    drag = True
                    prev_mouse_pos = pygame.mouse.get_pos()
                elif event.type == pygame.MOUSEBUTTONUP:
                    drag = False
            if drag:
                self.y_angle += (pygame.mouse.get_pos()[0] - prev_mouse_pos[0]) * self.ROTATE_SPEED
                self.x_angle += (pygame.mouse.get_pos()[1] - prev_mouse_pos[1]) * self.ROTATE_SPEED
                prev_mouse_pos = pygame.mouse.get_pos()
            glRotatef(0, 0, 0, 0)
            glClearColor(0.1, 0.1, 0.2, 0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.draw_cube(rubiks_cube)
            pygame.display.flip()
            pygame.time.Clock().tick(60)

    def draw_cube(self, cube):
        # Piece Color Order: Left, Right, Bottom, Top, Front, Back
        cube_pieces = [[ColorDict[cube.faces[36]], BLACK, BLACK, ColorDict[cube.faces[0]], BLACK, ColorDict[cube.faces[29]]],
                       [BLACK, BLACK, BLACK, ColorDict[cube.faces[1]], BLACK, ColorDict[cube.faces[28]]],
                       [BLACK, ColorDict[cube.faces[20]], BLACK, ColorDict[cube.faces[2]], BLACK, ColorDict[cube.faces[27]]],
                       [ColorDict[cube.faces[37]], BLACK, BLACK, ColorDict[cube.faces[3]], BLACK, BLACK],
                       [BLACK, BLACK, BLACK, ColorDict[cube.faces[4]], BLACK, BLACK],
                       [BLACK, ColorDict[cube.faces[19]], BLACK, ColorDict[cube.faces[5]], BLACK, BLACK],
                       [ColorDict[cube.faces[38]], BLACK, BLACK, ColorDict[cube.faces[6]], ColorDict[cube.faces[9]], BLACK],
                       [BLACK, BLACK, BLACK, ColorDict[cube.faces[7]], ColorDict[cube.faces[10]], BLACK],
                       [BLACK, ColorDict[cube.faces[18]], BLACK, ColorDict[cube.faces[8]], ColorDict[cube.faces[11]], BLACK],
                       [ColorDict[cube.faces[39]], BLACK, BLACK, BLACK, BLACK, ColorDict[cube.faces[32]]],
                       [BLACK, BLACK, BLACK, BLACK, BLACK, ColorDict[cube.faces[31]]],
                       [BLACK, ColorDict[cube.faces[23]], BLACK, BLACK, BLACK, ColorDict[cube.faces[30]]],
                       [ColorDict[cube.faces[40]], BLACK, BLACK, BLACK, BLACK, BLACK],
                       [BLACK, BLACK, BLACK, BLACK, BLACK, BLACK],
                       [BLACK, ColorDict[cube.faces[22]], BLACK, BLACK, BLACK, BLACK],
                       [ColorDict[cube.faces[41]], BLACK, BLACK, BLACK, ColorDict[cube.faces[12]], BLACK],
                       [BLACK, BLACK, BLACK, BLACK, ColorDict[cube.faces[13]], BLACK],
                       [BLACK, ColorDict[cube.faces[21]], BLACK, BLACK, ColorDict[cube.faces[14]], BLACK],
                       [ColorDict[cube.faces[42]], BLACK, ColorDict[cube.faces[45]], BLACK, BLACK, ColorDict[cube.faces[35]]],
                       [BLACK, BLACK, ColorDict[cube.faces[48]], BLACK, BLACK, ColorDict[cube.faces[34]]],
                       [BLACK, ColorDict[cube.faces[26]], ColorDict[cube.faces[51]], BLACK, BLACK, ColorDict[cube.faces[33]]],
                       [ColorDict[cube.faces[43]], BLACK, ColorDict[cube.faces[46]], BLACK, BLACK, BLACK],
                       [BLACK, BLACK, ColorDict[cube.faces[49]], BLACK, BLACK, BLACK],
                       [BLACK, ColorDict[cube.faces[25]], ColorDict[cube.faces[52]], BLACK, BLACK, BLACK],
                       [ColorDict[cube.faces[44]], BLACK, ColorDict[cube.faces[47]], BLACK, ColorDict[cube.faces[15]], BLACK],
                       [BLACK, BLACK, ColorDict[cube.faces[50]], BLACK, ColorDict[cube.faces[16]], BLACK],
                       [BLACK, ColorDict[cube.faces[24]], ColorDict[cube.faces[53]], BLACK, ColorDict[cube.faces[17]], BLACK]]
        for j in range(3):
            for k in range(3):
                for i in range(3):
                    self.draw_piece(-1.1 + (i * 1.1), 1.1 - (j * 1.1), -1.1 + (k * 1.1), cube_pieces[j * 9 + k * 3 + i])

    def draw_piece(self, cube_x, cube_y, cube_z, piece):
        w = 0.5
        vertices = [np.matrix([cube_x - w, cube_y - w, cube_z - w]), np.matrix([cube_x - w, cube_y + w, cube_z - w]),
                    np.matrix([cube_x - w, cube_y + w, cube_z + w]), np.matrix([cube_x - w, cube_y - w, cube_z + w]),
                    np.matrix([cube_x + w, cube_y - w, cube_z - w]), np.matrix([cube_x + w, cube_y + w, cube_z - w]),
                    np.matrix([cube_x + w, cube_y + w, cube_z + w]), np.matrix([cube_x + w, cube_y - w, cube_z + w])]
        edges = ((0, 1), (0, 3), (0, 4), (1, 2), (1, 5), (2, 3), (2, 6), (3, 7), (4, 5), (4, 7), (5, 6), (6, 7))
        faces = ((0, 1, 2, 3), (4, 5, 6, 7), (0, 4, 7, 3), (1, 5, 6, 2), (2, 6, 7, 3), (1, 5, 4, 0))

        rotation_x = np.matrix([[1, 0, 0], [0, cos(self.x_angle), -sin(self.x_angle)], [0, sin(self.x_angle), cos(self.x_angle)]])
        rotation_y = np.matrix([[cos(self.y_angle), 0, sin(self.y_angle)], [0, 1, 0], [-sin(self.y_angle), 0, cos(self.y_angle)]])
        rotation_z = np.matrix([[cos(self.z_angle), -sin(self.z_angle), 0], [sin(self.z_angle), cos(self.z_angle), 0], [0, 0, 1]])

        for i in range(len(vertices)):
            vertices[i] = np.dot(rotation_z, vertices[i].reshape((3, 1)))
            vertices[i] = np.dot(rotation_y, vertices[i])
            vertices[i] = np.dot(rotation_x, vertices[i])

        glBegin(GL_QUADS)
        for i in range(len(faces)):
            for vertex in faces[i]:
                glColor3fv(piece[i])
                glVertex3fv(vertices[vertex])
        glEnd()

        glBegin(GL_LINES)
        glColor3fv(BLACK)
        for edge in edges:
            for vertex in edge:
                glVertex3fv(vertices[vertex])
        glEnd()
