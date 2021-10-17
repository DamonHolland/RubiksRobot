import time
from datetime import timedelta
from model.RubiksCube import RubiksCube
from ai.RubiksSolver import solve, perform_move


def encode_to_input(cube) -> list:
    encoding = []
    for face_color in cube.faces:
        encoding += face_color
    return list(encoding)


def create_training_data(data_size, scramble_moves, cube=None):
    training_input = []
    training_output = []
    new_cube = cube if cube else RubiksCube()
    while len(training_input) < data_size:
        while new_cube.is_solved():
            new_cube.scramble(scramble_moves)
        solve_moves = solve(new_cube)
        for move in solve_moves:
            new_input = encode_to_input(new_cube)
            if training_input.count(new_input) == 0:
                training_input.append(new_input)
                training_output.append(move)
            perform_move(new_cube, move)
    return training_input, training_output


if __name__ == '__main__':
    start_time = time.time()
    create_training_data(10000, 3, cube=None)
    print("Data created in {}".format(timedelta(seconds=time.time() - start_time)))
