import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import time
from datetime import timedelta
from model.RubiksCube import RubiksCube
from ai.RubiksSolver import solve, perform_move
import numpy as np


def encode_to_input(cube) -> list:
    encoding = []
    for face_color in cube.faces:
        encoding += face_color
    return list(encoding)


def create_categorical_training_data(data_size, scramble_moves):
    training_data = dict()
    fail_count = 0
    training_data[RubiksCube()] = 0
    while len(training_data.items()) < data_size:
        # Scramble the cube
        new_cube = RubiksCube()
        while new_cube.is_solved():
            new_cube.scramble(scramble_moves)
        # Solve the cube
        solve_moves = solve(new_cube)
        # Loop through all moves to solve, popping off each iteration
        while len(solve_moves) > 0:
            try:
                # If the cube state already exists, end this solve
                _check_exists = training_data[new_cube]
                fail_count += 1
                break
            except KeyError:
                # If the cube state does not already exist in the input data, continue
                training_data[new_cube] = len(solve_moves)
                perform_move(new_cube, solve_moves.pop(0))
                fail_count = 0
        # To break if there arent as many permutations as there is requested data
        # Will fail if all fails to find new data 10 times in a row
        if fail_count > 10:
            data_size = len(training_data)
            print("Requested Data too large, not enough permutations. Only {} Found".format(len(training_data)))
            print("Requesting more data than permutations can lead to slower data generation.")

    nn_input = np.array([encode_to_input(key) for key in list(training_data.keys())])
    nn_output = np.array(list(training_data.values()))
    shuffle = np.random.permutation(len(training_data))
    return np.array(nn_input)[shuffle], np.array(nn_output)[shuffle]


if __name__ == '__main__':
    start_time = time.time()
    SCRAMBLE_TEST = 7
    x, y = create_categorical_training_data(4096, SCRAMBLE_TEST)
    max_moves = max(y) + 1
    print("Data created in {}".format(timedelta(seconds=time.time() - start_time)))
    print("Required nodes for {} moves is {}".format(SCRAMBLE_TEST, max_moves))
