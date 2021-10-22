import kociemba
from model.RubiksCube import RubiksCube
from RubiksMoves import MoveDecoder, MoveEncoder


def perform_move(cube: RubiksCube, move):
    if move == 0:
        cube.rotate_white()
    elif move == 1:
        cube.rotate_white(True)
    elif move == 2:
        cube.rotate_green()
    elif move == 3:
        cube.rotate_green(True)
    elif move == 4:
        cube.rotate_red()
    elif move == 5:
        cube.rotate_red(True)
    elif move == 6:
        cube.rotate_blue()
    elif move == 7:
        cube.rotate_blue(True)
    elif move == 8:
        cube.rotate_orange()
    elif move == 9:
        cube.rotate_orange(True)
    elif move == 10:
        cube.rotate_yellow()
    elif move == 11:
        cube.rotate_yellow(True)


def solve(cube: RubiksCube):
    # Reformat cube string to match kociemba input
    cube_string = cube.as_string().replace('W', 'U').replace('G', 'F').replace('Y', 'D').replace('O', 'L')
    # Use kociemba to solve cube, split string into a list of solves
    solve = kociemba.solve(cube_string).split(' ')
    # Replace the unsupported moves into moves that our NN can output
    for i, item in list(enumerate(solve))[::-1]:
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
    # encode the moves into a format the NN can accept
    for i in range(len(solve)):
        solve[i] = MoveEncoder[solve[i]]
    return solve


if __name__ == "__main__":
    rubiks_cube = RubiksCube()
    rubiks_cube.scramble(50)
    solve_move = solve(rubiks_cube)
    move_count = 0
    for move in solve_move:
        move = MoveDecoder[move]
        move_count += 1
        print("Performing Move {}: {}".format(move_count, move))
        perform_move(rubiks_cube, move)
    print("Cube solved in {} moves with Kociembas algorithm".format(move_count))
