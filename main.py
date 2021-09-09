import pygame
import numpy as np
import Colors
import RubiksCube
from pygame.locals import *
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *

WINDOW_HEIGHT = 720
WINDOW_WIDTH = 720
ROTATE_SPEED = 0.005
x_angle = 0
y_angle = 0
z_angle = 0


def draw_cube(cube):
    piece_index = 0
    for j in range(3):
        for k in range(3):
            for i in range(3):
                draw_piece(-1.1 + (i * 1.1), 1.1 - (j * 1.1), -1.1 + (k * 1.1), cube.pieces[piece_index])
                piece_index += 1


def draw_piece(cube_x, cube_y, cube_z, piece):
    width = 0.5
    vertices = (
        np.matrix([cube_x - width, cube_y - width, cube_z - width]),
        np.matrix([cube_x - width, cube_y + width, cube_z - width]),
        np.matrix([cube_x - width, cube_y + width, cube_z + width]),
        np.matrix([cube_x - width, cube_y - width, cube_z + width]),
        np.matrix([cube_x + width, cube_y - width, cube_z - width]),
        np.matrix([cube_x + width, cube_y + width, cube_z - width]),
        np.matrix([cube_x + width, cube_y + width, cube_z + width]),
        np.matrix([cube_x + width, cube_y - width, cube_z + width])
    )
    edges = ((0, 1), (0, 3), (0, 4), (1, 2), (1, 5), (2, 3), (2, 6), (3, 7), (4, 5), (4, 7), (5, 6), (6, 7))
    faces = ((0, 1, 2, 3), (4, 5, 6, 7), (0, 4, 7, 3), (1, 5, 6, 2), (2, 6, 7, 3), (1, 5, 4, 0))

    rotation_x = np.matrix([[1, 0, 0], [0, cos(x_angle), -sin(x_angle)], [0, sin(x_angle), cos(x_angle)]])
    rotation_y = np.matrix([[cos(y_angle), 0, sin(y_angle)], [0, 1, 0], [-sin(y_angle), 0, cos(y_angle)]])
    rotation_z = np.matrix([[cos(z_angle), -sin(z_angle), 0], [sin(z_angle), cos(z_angle), 0], [0, 0, 1]])

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
            glColor3fv(piece.colors[color_index])
            glVertex3fv(rotated_points[vertex])
        color_index += 1
    glEnd()

    glBegin(GL_LINES)
    glColor3fv(Colors.BLACK)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(rotated_points[vertex])
    glEnd()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF | OPENGL)
    gluPerspective(45, WINDOW_WIDTH/WINDOW_HEIGHT, 0.1, 50.0)
    glEnable(GL_DEPTH_TEST)
    glTranslatef(0.0, 0.0, -8)
    pygame.display.set_caption("Rubik's Cube")
    running = True
    drag = False
    prev_mouse_pos = [0, 0]
    rubiks_cube = RubiksCube.RubiksCube()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                drag = True
                prev_mouse_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                drag = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    rubiks_cube.U()
        if drag:
            new_pos = pygame.mouse.get_pos()
            y_angle += (new_pos[0] - prev_mouse_pos[0]) * ROTATE_SPEED
            x_angle += (new_pos[1] - prev_mouse_pos[1]) * ROTATE_SPEED
            prev_mouse_pos = new_pos
        glRotatef(0, 0, 0, 0)
        glClearColor(0.1, 0.1, 0.2, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_cube(rubiks_cube)
        pygame.display.flip()
        pygame.time.Clock().tick(60)
