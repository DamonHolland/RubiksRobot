from model.RubiksCube import RubiksCube

MoveDecoder = {0: "U",
               1: "U'",
               2: "F",
               3: "F'",
               4: "R",
               5: "R'",
               6: "B",
               7: "B'",
               8: "L",
               9: "L'",
               10: "D",
               11: "D'",
               }

MoveEncoder = {"U": 0,
               "U'": 1,
               "F": 2,
               "F'": 3,
               "R": 4,
               "R'": 5,
               "B": 6,
               "B'": 7,
               "L": 8,
               "L'": 9,
               "D": 10,
               "D'": 11}


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


def move_reverse(move):
    return move + 1 if move % 2 == 0 else move - 1


def encode_to_input(cube) -> list:
    return [item for t in cube.faces for item in t]
