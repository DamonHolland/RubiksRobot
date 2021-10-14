from model.RubiksCube import RubiksCube

def encode_to_input(cube) -> list:
    encoding = []
    for face_color in cube.faces:
        encoding += face_color
    return list(encoding)

def create_training_data(data_size, scramble_moves):
    training_input = []
    training_output = []
    for i in range(data_size):
        new_cube = RubiksCube()
        new_cube.scramble(scramble_moves)
        training_input.append(encode_to_input(new_cube))
        training_output.append(new_cube.last_move + 1 if new_cube.last_move % 2 == 0 else new_cube.last_move - 1)
    return training_input, training_output