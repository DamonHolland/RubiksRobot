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
    training_input = []
    training_output = []
    fail_count = 0
    while len(training_input) < data_size:
        new_cube = RubiksCube()
        while new_cube.is_solved():
            new_cube.scramble(scramble_moves)
        solve_moves = solve(new_cube)
        for move in solve_moves:
            new_input = encode_to_input(new_cube)
            if training_input.count(new_input) == 0:
                training_input.append(new_input)
                training_output.append(move)
                perform_move(new_cube, move)
                fail_count = 0
            else:
                fail_count += 1
                break
        # To break if there arent as many permutations as there is requested data
        # Will Fail if all fails to find new data 10 times in a row
        if fail_count > 10:
            data_size = len(training_input)
            print("Requested Data too large, not enough permutations. Only {} Found".format(len(training_input)))
    return np.array(training_input), np.array(training_output)


if __name__ == '__main__':
    start_time = time.time()
    create_training_data(10000, 5)
    print("Data created in {}".format(timedelta(seconds=time.time() - start_time)))
