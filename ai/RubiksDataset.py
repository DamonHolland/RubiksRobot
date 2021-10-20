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


def create_training_data(data_size, scramble_moves):
    training_data = dict()
    fail_count = 0
    while len(training_data.items()) < data_size:
        new_cube = RubiksCube()
        while new_cube.is_solved():
            new_cube.scramble(scramble_moves)
        solve_moves = solve(new_cube)
        for move in solve_moves:
            new_input = encode_to_input(new_cube)
            try:
                check_exists = training_data[str(new_input)]
                fail_count += 1
                break
            except KeyError:
                training_data[str(new_input)] = move
                perform_move(new_cube, move)
                fail_count = 0
        # To break if there arent as many permutations as there is requested data
        # Will fail if all fails to find new data 10 times in a row
        if fail_count > 10:
            data_size = len(training_data.items())
            print("Requested Data too large, not enough permutations. Only {} Found".format(len(training_data.items())))
    input = []
    output = []
    for key, value in training_data.items():
        input.append(key)
        output.append(value)
    shuffle = np.random.permutation(len(input))
    return np.array(input)[shuffle], np.array(output)[shuffle]


if __name__ == '__main__':
    start_time = time.time()
    create_training_data(10000, 5)
    print("Data created in {}".format(timedelta(seconds=time.time() - start_time)))
