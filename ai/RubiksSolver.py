import time

import kociemba
from model.RubiksCube import RubiksCube
# from visuals.RubiksVisualizer import RubiksVisualizer
from RubiksMoves import MoveDecoder, MoveEncoder

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

def solve(cube: RubiksCube):
    cube_string = cube.as_string().replace('W', 'U').replace('G', 'F').replace('Y', 'D').replace('O', 'L')
    solve = kociemba.solve(cube_string).split(' ')
    for i, item in list(enumerate(solve))[::-1]:  # makes and copy and reverse it (IMPORTANT!)
        if item == 'U2':
            solve[i:i + 1] = ['U', 'U']
        elif item == 'F2':
            solve[i:i + 1] = ['F', 'F']
        elif item == 'R2':
            solve[i:i + 1] = ['R', 'R']
        elif item == 'L2':
            solve[i:i + 1] = ['L', 'L']
        elif item == 'B2':
            solve[i:i + 1] = ['B', 'B']
        elif item == 'D2':
            solve[i:i + 1] = ['D', 'D']
    for i in range(len(solve)):
        solve[i] = MoveEncoder[solve[i]]
    return solve

# if __name__ == "__main__":
#     rubiks_cube = RubiksCube()
#     rubiks_cube.scramble(50)
#     RubiksVisualizer(rubiks_cube)
#     time.sleep(2)
#     solve_move = solve(rubiks_cube)
#     move_count = 0
#     for move in solve_move:
#         move = MoveDecoder[move]
#         move_count += 1
#         print("Performing Move {}: {}".format(move_count, move))
#         time.sleep(0.05)
#         perform_move(rubiks_cube, move)
#     print("Cube solved in {} moves with Kociembas algorithm".format(move_count))