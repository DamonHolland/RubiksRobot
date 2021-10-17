import time
import ai.RubiksDataset as data
from ai.RubiksSolver import perform_move
from ai.RubiksMoves import MoveDecoder
from model.RubiksCube import RubiksCube
from visuals.RubiksVisualizer import RubiksVisualizer
import tensorflow as tf

if __name__ == '__main__':
    NUM_SCRAMBLES = 3
    MODEL_NAME = "2_1.0_0.00021674610616173595"
    model = tf.keras.models.load_model("models/" + MODEL_NAME)

    print("\nSingle Solve Test\n")
    cube = RubiksCube()
    RubiksVisualizer(cube)
    cube.scramble(NUM_SCRAMBLES)
    print("Cube scrambled {} moves.".format(NUM_SCRAMBLES))
    time.sleep(1)
    MAX_MOVES = 30
    num_moves = 0
    while not cube.is_solved() and num_moves < MAX_MOVES:
        num_moves += 1
        prediction = list(model.predict([data.encode_to_input(cube)])[0])
        time.sleep(0.1)
        prediction_move = prediction.index(max(prediction))
        perform_move(cube, prediction_move)
        print("AI predicts move {}".format(MoveDecoder[prediction_move]))
    if cube.is_solved():
        print("AI Solved cube in {} Moves.".format(num_moves))
    else:
        print("AI failed to solve cube within {} Moves.".format(MAX_MOVES))
