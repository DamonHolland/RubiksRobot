import pygame
import numpy as np
from math import *

WINDOW_HEIGHT = 720
WINDOW_WIDTH = 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
SCALE = 100
ROTATE_SPEED = 0.005
x_angle = 90
y_angle = 90
z_angle = 0
drag = False

def draw_cube(cube_x, cube_y, cube_z):
    width = 0.5
    points = [np.matrix([cube_x + width, cube_y + width, cube_z + width]),
              np.matrix([cube_x + width, cube_y + width, cube_z - width]),
              np.matrix([cube_x + width, cube_y - width, cube_z + width]),
              np.matrix([cube_x + width, cube_y - width, cube_z - width]),
              np.matrix([cube_x - width, cube_y + width, cube_z + width]),
              np.matrix([cube_x - width, cube_y + width, cube_z - width]),
              np.matrix([cube_x - width, cube_y - width, cube_z + width]),
              np.matrix([cube_x - width, cube_y - width, cube_z - width])]
    rotation_x = np.matrix([[1, 0, 0], [0, cos(x_angle), -sin(x_angle)], [0, sin(x_angle), cos(x_angle)]])
    rotation_y = np.matrix([[cos(y_angle), 0, sin(y_angle)], [0, 1, 0], [-sin(y_angle), 0, cos(y_angle)]])
    rotation_z = np.matrix([[cos(z_angle), -sin(z_angle), 0], [sin(z_angle), cos(z_angle), 0],[0, 0, 1]])

    projected_points = []
    for point in points:
        rotated2d = np.dot(rotation_z, point.reshape((3, 1)))
        rotated2d = np.dot(rotation_y, rotated2d)
        rotated2d = np.dot(rotation_x, rotated2d)
        projected2d = np.dot(np.matrix([[1, 0, 0], [0, 1, 0]]), rotated2d)
        x = int(projected2d[0][0] * SCALE) + WINDOW_WIDTH / 2
        y = int(projected2d[1][0] * SCALE) + WINDOW_HEIGHT / 2
        projected_points.append([x, y])

    for i in range(8):
        for j in range(i + 1, 8):
            if dist(points[i].reshape((3, 1)), points[j].reshape((3, 1))) == 1:
                pygame.draw.line(screen, BLACK, projected_points[i], projected_points[j])


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Rubik's Cube")
    running = True
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
            y_angle += (new_pos[0] - prev_mouse_pos[0]) * ROTATE_SPEED
            x_angle += (new_pos[1] - prev_mouse_pos[1]) * ROTATE_SPEED
            prev_mouse_pos = new_pos

        screen.fill(WHITE)
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    draw_cube(-1 + i, -1 + j, -1 + k)
        pygame.display.update()
        pygame.time.Clock().tick(60)
