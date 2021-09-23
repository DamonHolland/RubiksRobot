from model.RubiksCube import RubiksCube

EncodingDict = {RubiksCube.WHITE: [0, 0, 0],
             RubiksCube.GREEN: [0, 0, 1],
             RubiksCube.RED: [0, 1, 0],
             RubiksCube.BLUE: [0, 1, 1],
             RubiksCube.ORANGE: [1, 0, 0],
             RubiksCube.YELLOW: [1, 0, 1]}

def encode_to_input(cube) -> list:
    encoding = []
    for face_color in cube.faces:
        for neuron in EncodingDict[face_color]:
            encoding.append(neuron)
    return list(encoding)

def createTrainingData(data_size, scramble_moves):
    training_input = []
    training_output = []
    for i in range(data_size):
        new_cube = RubiksCube()
        new_cube.scramble(scramble_moves)
        training_input.append(encode_to_input(new_cube))
        if new_cube.last_move % 2 == 0:
            inverse_move = new_cube.last_move + 1
        else:
            inverse_move = new_cube.last_move - 1
        training_output.append(inverse_move)
    return training_input, training_output