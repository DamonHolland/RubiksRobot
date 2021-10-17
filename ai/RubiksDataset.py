import random
import time
from datetime import timedelta

from model.RubiksCube import RubiksCube
from ai.RubiksSolver import solve


def encode_to_input(cube) -> list:
    encoding = []
    for face_color in cube.faces:
        encoding += face_color
    return list(encoding)


def create_training_data(data_size, scramble_moves, cube=None):
    training_input = []
    training_output = []
    for i in range(data_size):
        new_cube = cube if cube else RubiksCube()
        while new_cube.is_solved():
            new_cube.scramble(random.randint(1, scramble_moves))
        training_input.append(encode_to_input(new_cube))
        solve_moves = solve(new_cube)
        training_output.append(solve_moves[0])
    return training_input, training_output

if __name__ == '__main__':
    start_time = time.time()
    create_training_data(10000, 3, cube=None)
    print("Data created in {}".format(timedelta(seconds=time.time() - start_time)))

