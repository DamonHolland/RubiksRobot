import time
import ai.RubiksDataset as Data
from ai.RubiksMoves import MoveDecoder
from model.RubiksCube import RubiksCube
from visuals.RubiksVisualizer import RubiksVisualizer
import tensorflow as tf

if __name__ == '__main__':
    NUM_SCRAMBLES = 3
    MODEL_NAME = "2_1.0_0.053325917571783066"
    EVALUATION_COUNT = 10
    MAX_MOVES = 30
    model = tf.keras.models.load_model("models/" + MODEL_NAME)

    print("\nEvaluating Model\n")
    success_solves = 0
    for i in range(EVALUATION_COUNT):
        cube = RubiksCube()
        cube.scramble(NUM_SCRAMBLES)
        num_moves = 0
        while not cube.is_solved() and num_moves < MAX_MOVES:
            num_moves += 1
            prediction = list(model.predict([Data.encode_to_input(cube)])[0])
            prediction_move = prediction.index(max(prediction))
            Data.perform_move(cube, prediction_move)
        if cube.is_solved():
            success_solves += 1
    print("Model Solved Cube in {} out of {} attempts.".format(success_solves, EVALUATION_COUNT))

    print("\nSingle Solve Test\n")
    cube = RubiksCube()
    RubiksVisualizer(cube)
    cube.scramble(NUM_SCRAMBLES)
    print("Cube scrambled {} moves.".format(NUM_SCRAMBLES))
    time.sleep(1)
    num_moves = 0
    while not cube.is_solved() and num_moves < MAX_MOVES:
        num_moves += 1
        prediction = list(model.predict([Data.encode_to_input(cube)])[0])
        time.sleep(0.1)
        prediction_move = prediction.index(max(prediction))
        Data.perform_move(cube, prediction_move)
        print("AI predicts move {}".format(MoveDecoder[prediction_move]))
    if cube.is_solved():
        print("AI Solved cube in {} Moves.".format(num_moves))
    else:
        print("AI failed to solve cube within {} Moves.".format(MAX_MOVES))
