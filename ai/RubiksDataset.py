import time
from datetime import timedelta
from model.RubiksCube import RubiksCube

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

def encode_to_input(cube) -> list:
    encoding = []
    for face_color in cube.faces:
        encoding += face_color
    return list(encoding)


def create_training_data(data_size, scramble_moves, cube=None):
    training_input = []
    training_output = []
    fail_count = 0
    new_cube = cube if cube else RubiksCube()
    while len(training_input) < data_size:
        while new_cube.is_solved():
            scramble = []
            for i in range(scramble_moves):
                new_cube.scramble(1)
                scramble.append(new_cube.last_move)
        scramble.reverse()
        solve_moves = scramble
        for move in solve_moves:
            new_input = encode_to_input(new_cube)
            if training_input.count(new_input) == 0:
                training_input.append(new_input)
                training_output.append(move)
                fail_count = 0
            else:
                fail_count += 1
            perform_move(new_cube, move)
        # To break if there arent as many permutations as there is requested data
        if fail_count > data_size:
            data_size = len(training_input)
            print("Requested Data too large, not enough permutations")
    return training_input, training_output


if __name__ == '__main__':
    start_time = time.time()
    create_training_data(10000, 3, cube=None)
    print("Data created in {}".format(timedelta(seconds=time.time() - start_time)))
