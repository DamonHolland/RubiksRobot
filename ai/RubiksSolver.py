import time

import kociemba
from model.RubiksCube import RubiksCube
from visuals.RubiksVisualizer import RubiksVisualizer

def perform_move(cube: RubiksCube, move):
    if move == "U":
        cube.rotate_white()
    elif move == "U'":
        cube.rotate_white(True)
    elif move == "F":
        cube.rotate_green()
    elif move == "F'":
        cube.rotate_green(True)
    elif move == "R":
        cube.rotate_red()
    elif move == "R'":
        cube.rotate_red(True)
    elif move == "B":
        cube.rotate_blue()
    elif move == "B'":
        cube.rotate_blue(True)
    elif move == "L":
        cube.rotate_orange()
    elif move == "L'":
        cube.rotate_orange(True)
    elif move == "D":
        cube.rotate_yellow()
    elif move == "D'":
        cube.rotate_yellow(True)
    elif move == "U2":
        cube.rotate_white()
        cube.rotate_white()
    elif move == "F2":
        cube.rotate_green()
        cube.rotate_green()
    elif move == "R2":
        cube.rotate_red()
        cube.rotate_red()
    elif move == "B2":
        cube.rotate_blue()
        cube.rotate_blue()
    elif move == "L2":
        cube.rotate_orange()
        cube.rotate_orange()
    elif move == "D2":
        cube.rotate_yellow()
        cube.rotate_yellow()

def solve(cube: RubiksCube):
    cube_string = cube.as_string().replace('W', 'U').replace('G', 'F').replace('Y', 'D').replace('O', 'L')
    print(cube_string)
    solve_moves = kociemba.solve(cube_string).split(' ')
    move_count = 0
    for move in solve_moves:
        move_count += 1
        print("Performing Move {}".format(move_count))
        time.sleep(1)
        perform_move(cube, move)
    print("Cube solved in {} moves with Kociembas algorithm".format(move_count))

if __name__ == "__main__":
    rubiks_cube = RubiksCube()
    rubiks_cube.scramble(1000)
    RubiksVisualizer(rubiks_cube)
    time.sleep(3)
    solve(rubiks_cube)