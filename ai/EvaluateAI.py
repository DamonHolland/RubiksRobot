import sys
import os.path

from numpy.lib.function_base import copy
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import time
import ai.RubiksDataset as data
import ai.RubiksSolver as solver
from ai.RubiksMoves import MoveDecoder
from model.RubiksCube import RubiksCube
from visuals.RubiksVisualizer import RubiksVisualizer
import tensorflow as tf
import numpy as np
import copy

def get_categorical_prediction(prediction_model, cube):
            predictions = prediction_model(np.array([data.encode_to_input(cube)]))[0]
            return np.argmax(predictions, axis=0) + 1

if __name__ == '__main__':
    NUM_SCRAMBLES = 3
    MODEL_NAME = "5_0.98828125_0.07847923040390015"
    MAX_MOVES = 30
    model = tf.keras.models.load_model("models/" + MODEL_NAME)

    print("\nEvaluating Model\n")
    total_solves = 0
    success_solves = 0
    rubiks_cube = RubiksCube()
    visual_cube = RubiksCube()
    RubiksVisualizer(visual_cube)
    while True:
        solve_visual_moves = []
        move_count = 0
        last_move_reverse = -1
        rubiks_cube = RubiksCube()
        rubiks_cube.scramble(NUM_SCRAMBLES)
        visual_cube.faces = copy.copy(rubiks_cube.faces)
        while not rubiks_cube.is_solved() and move_count < MAX_MOVES:
            next_solve_minimum = 100
            minimum_move = 0
            for key, value in MoveDecoder.items():
                if key != last_move_reverse:
                    solver.perform_move(rubiks_cube, key)
                    if rubiks_cube.is_solved():
                        next_solve_minimum = -1
                        minimum_move = key
                    else:
                        prediction = get_categorical_prediction(model, rubiks_cube)
                        if prediction < next_solve_minimum:
                            next_solve_minimum = prediction
                            minimum_move = key
                    solver.perform_move(rubiks_cube, key + 1 if key % 2 == 0 else key - 1)
            move_count += 1
            last_move_reverse = minimum_move + 1 if minimum_move % 2 == 0 else minimum_move - 1
            solve_visual_moves.append(minimum_move)
            solver.perform_move(rubiks_cube, minimum_move)
        total_solves += 1
        for move in solve_visual_moves:
            solver.perform_move(visual_cube, move)
            # time.sleep(0.3)
        if (rubiks_cube.is_solved()):
            print("AI Solved cube in {} Moves".format(move_count))
            success_solves += 1
        else:
            print("AI Failed to solve cube in {} Moves".format(MAX_MOVES))
        print("AI Solved Cube {} out of {} times.".format(success_solves, total_solves))
        # time.sleep(1)
