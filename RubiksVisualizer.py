import pygame
import numpy as np

import Colors
from Colors import ColorDict
from pygame.locals import *
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *


class RubiksVisualizer:
    WINDOW_HEIGHT = 720
    WINDOW_WIDTH = 720
    ROTATE_SPEED = 0.005
    x_angle = 0
    y_angle = 0
    z_angle = 0

    def __init__(self, rubiks_cube):
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
                new_pos = pygame.mouse.get_pos()
                self.y_angle += (new_pos[0] - prev_mouse_pos[0]) * self.ROTATE_SPEED
                self.x_angle += (new_pos[1] - prev_mouse_pos[1]) * self.ROTATE_SPEED
                prev_mouse_pos = new_pos
            glRotatef(0, 0, 0, 0)
            glClearColor(0.1, 0.1, 0.2, 0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.draw_cube(rubiks_cube)
            pygame.display.flip()
            pygame.time.Clock().tick(60)

    def draw_cube(self, cube):
        # Piece Color Order: Left, Right, Bottom, Top, Front, Back
        cube_pieces = [[ColorDict[cube.faces[36]], Colors.BLACK, Colors.BLACK, ColorDict[cube.faces[0]], Colors.BLACK, ColorDict[cube.faces[29]]],
                       [Colors.BLACK, Colors.BLACK, Colors.BLACK, ColorDict[cube.faces[1]], Colors.BLACK, ColorDict[cube.faces[28]]],
                       [Colors.BLACK, ColorDict[cube.faces[20]], Colors.BLACK, ColorDict[cube.faces[2]], Colors.BLACK, ColorDict[cube.faces[27]]],
                       [ColorDict[cube.faces[37]], Colors.BLACK, Colors.BLACK, ColorDict[cube.faces[3]], Colors.BLACK, Colors.BLACK],
                       [Colors.BLACK, Colors.BLACK, Colors.BLACK, ColorDict[cube.faces[4]], Colors.BLACK, Colors.BLACK],
                       [Colors.BLACK, ColorDict[cube.faces[19]], Colors.BLACK, ColorDict[cube.faces[5]], Colors.BLACK, Colors.BLACK],
                       [ColorDict[cube.faces[38]], Colors.BLACK, Colors.BLACK, ColorDict[cube.faces[6]], ColorDict[cube.faces[9]], Colors.BLACK],
                       [Colors.BLACK, Colors.BLACK, Colors.BLACK, ColorDict[cube.faces[7]], ColorDict[cube.faces[10]], Colors.BLACK],
                       [Colors.BLACK, ColorDict[cube.faces[18]], Colors.BLACK, ColorDict[cube.faces[8]], ColorDict[cube.faces[11]], Colors.BLACK],
                       [ColorDict[cube.faces[39]], Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.BLACK, ColorDict[cube.faces[32]]],
                       [Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.BLACK, ColorDict[cube.faces[31]]],
                       [Colors.BLACK, ColorDict[cube.faces[23]], Colors.BLACK, Colors.BLACK, Colors.BLACK, ColorDict[cube.faces[30]]],
                       [ColorDict[cube.faces[40]], Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.BLACK],
                       [Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.BLACK],
                       [Colors.BLACK, ColorDict[cube.faces[22]], Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.BLACK],
                       [ColorDict[cube.faces[41]], Colors.BLACK, Colors.BLACK, Colors.BLACK, ColorDict[cube.faces[12]], Colors.BLACK],
                       [Colors.BLACK, Colors.BLACK, Colors.BLACK, Colors.BLACK, ColorDict[cube.faces[13]], Colors.BLACK],
                       [Colors.BLACK, ColorDict[cube.faces[21]], Colors.BLACK, Colors.BLACK, ColorDict[cube.faces[14]], Colors.BLACK],
                       [ColorDict[cube.faces[42]], Colors.BLACK, ColorDict[cube.faces[45]], Colors.BLACK, Colors.BLACK, ColorDict[cube.faces[35]]],
                       [Colors.BLACK, Colors.BLACK, ColorDict[cube.faces[48]], Colors.BLACK, Colors.BLACK, ColorDict[cube.faces[34]]],
                       [Colors.BLACK, ColorDict[cube.faces[26]], ColorDict[cube.faces[51]], Colors.BLACK, Colors.BLACK, ColorDict[cube.faces[33]]],
                       [ColorDict[cube.faces[43]], Colors.BLACK, ColorDict[cube.faces[46]], Colors.BLACK, Colors.BLACK, Colors.BLACK],
                       [Colors.BLACK, Colors.BLACK, ColorDict[cube.faces[49]], Colors.BLACK, Colors.BLACK, Colors.BLACK],
                       [Colors.BLACK, ColorDict[cube.faces[25]], ColorDict[cube.faces[52]], Colors.BLACK, Colors.BLACK, Colors.BLACK],
                       [ColorDict[cube.faces[44]], Colors.BLACK, ColorDict[cube.faces[47]], Colors.BLACK, ColorDict[cube.faces[15]], Colors.BLACK],
                       [Colors.BLACK, Colors.BLACK, ColorDict[cube.faces[50]], Colors.BLACK, ColorDict[cube.faces[16]], Colors.BLACK],
                       [Colors.BLACK, ColorDict[cube.faces[24]], ColorDict[cube.faces[53]], Colors.BLACK, ColorDict[cube.faces[17]], Colors.BLACK]]
        piece_index = 0
        for j in range(3):
            for k in range(3):
                for i in range(3):
                    self.draw_piece(-1.1 + (i * 1.1), 1.1 - (j * 1.1), -1.1 + (k * 1.1), cube_pieces[piece_index])
                    piece_index += 1

    def draw_piece(self, cube_x, cube_y, cube_z, piece):
        width = 0.5
        vertices = (np.matrix([cube_x - width, cube_y - width, cube_z - width]),
                    np.matrix([cube_x - width, cube_y + width, cube_z - width]),
                    np.matrix([cube_x - width, cube_y + width, cube_z + width]),
                    np.matrix([cube_x - width, cube_y - width, cube_z + width]),
                    np.matrix([cube_x + width, cube_y - width, cube_z - width]),
                    np.matrix([cube_x + width, cube_y + width, cube_z - width]),
                    np.matrix([cube_x + width, cube_y + width, cube_z + width]),
                    np.matrix([cube_x + width, cube_y - width, cube_z + width]))
        edges = ((0, 1), (0, 3), (0, 4), (1, 2), (1, 5), (2, 3), (2, 6), (3, 7), (4, 5), (4, 7), (5, 6), (6, 7))
        faces = ((0, 1, 2, 3), (4, 5, 6, 7), (0, 4, 7, 3), (1, 5, 6, 2), (2, 6, 7, 3), (1, 5, 4, 0))

        rotation_x = np.matrix([[1, 0, 0], [0, cos(self.x_angle), -sin(self.x_angle)], [0, sin(self.x_angle), cos(self.x_angle)]])
        rotation_y = np.matrix([[cos(self.y_angle), 0, sin(self.y_angle)], [0, 1, 0], [-sin(self.y_angle), 0, cos(self.y_angle)]])
        rotation_z = np.matrix([[cos(self.z_angle), -sin(self.z_angle), 0], [sin(self.z_angle), cos(self.z_angle), 0], [0, 0, 1]])

        rotated_points = []
        for vertex in vertices:
            rotated_vertex = np.dot(rotation_z, vertex.reshape((3, 1)))
            rotated_vertex = np.dot(rotation_y, rotated_vertex)
            rotated_vertex = np.dot(rotation_x, rotated_vertex)
            rotated_points.append(rotated_vertex)

        glBegin(GL_QUADS)
        color_index = 0
        for face in faces:
            for vertex in face:
                glColor3fv(piece[color_index])
                glVertex3fv(rotated_points[vertex])
            color_index += 1
        glEnd()

        glBegin(GL_LINES)
        glColor3fv(Colors.BLACK)
        for edge in edges:
            for vertex in edge:
                glVertex3fv(rotated_points[vertex])
        glEnd()
