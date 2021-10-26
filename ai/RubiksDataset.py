import random
import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import time
from datetime import timedelta
from model.RubiksCube import RubiksCube
import numpy as np


def encode_to_input(cube) -> list:
    encoding = []
    for face_color in cube.faces:
        encoding += face_color
    return list(encoding)


def create_scramble_data(data_size, scramble_moves):
    training_data = dict()
    fail_count = 0
    while len(training_data.items()) < data_size:
        # Scramble the cube
        new_cube = RubiksCube()
        scramble_choice = random.randint(1, scramble_moves)
        while new_cube.is_solved():
            new_cube.scramble(scramble_choice)
        try:
            # If the cube state already exists, end this solve
            _check_exists = training_data[tuple(encode_to_input(new_cube))]
            fail_count += 1
        except KeyError:
            # If the cube state does not already exist in the input data, continue
            training_data[tuple(encode_to_input(new_cube))] = scramble_choice - 1
            fail_count = 0
        # To break if there arent as many permutations as there is requested data
        # Will fail if fails to find new data many times in a row
        if fail_count > data_size:
            print("Requested Data too large, not enough permutations. Only {} Found".format(len(training_data)))
            print("Requesting more data than permutations can lead to slower data generation.")
            break
    nn_input = np.array([list(key) for key in list(training_data.keys())])
    nn_output = np.array(list(training_data.values()))
    shuffle = np.random.permutation(len(training_data))
    return np.array(nn_input)[shuffle], np.array(nn_output)[shuffle]


if __name__ == '__main__':
    start_time = time.time()
    SCRAMBLE_TEST = 5
    x, y = create_scramble_data(10000, SCRAMBLE_TEST)
    print("Data created in {}".format(timedelta(seconds=time.time() - start_time)))
