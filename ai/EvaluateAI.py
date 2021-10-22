import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import ai.RubiksDataset as Data
import ai.RubiksSolver as Solver
from ai.RubiksMoves import MoveDecoder
from model.RubiksCube import RubiksCube
from visuals.RubiksVisualizer import RubiksVisualizer
import tensorflow as tf
import numpy as np
import copy


def get_categorical_prediction(prediction_model, cube) -> int:
    # Gets the numerical prediction from the neural network
    # This value is the estimated number of solves left
    predictions = prediction_model(np.array([Data.encode_to_input(cube)]))[0]
    return np.argmax(predictions, axis=0) + 1


if __name__ == '__main__':
    # Evaluation Config
    NUM_SCRAMBLES = 5
    MAX_MOVES = 30
    # Load Model
    MODEL_NAME = "5_0.99609375_0.01692289113998413"
    model = tf.keras.models.load_model("models/" + MODEL_NAME)

    print("\nEvaluating Model\n")
    total_solves = 0
    success_solves = 0
    rubiks_cube = RubiksCube()
    visual_cube = RubiksCube()
    RubiksVisualizer(visual_cube)
    # Evaluates until you exit the program
    while True:
        solve_visual_moves = []
        move_count = 0
        last_move_reverse = -1
        rubiks_cube = RubiksCube()
        rubiks_cube.scramble(NUM_SCRAMBLES)
        visual_cube.faces = copy.copy(rubiks_cube.faces)
        # Attempts moves until the cube is solved or attempts run out
        while not rubiks_cube.is_solved() and move_count < MAX_MOVES:
            next_solve_minimum = 100
            minimum_move = 0
            # Loop through each possible move
            for key in MoveDecoder.keys():
                # Don't attempt the reverse of the previous move, will just end up in a loop
                if key == last_move_reverse:
                    continue
                # Perform the move on the cube, then evaluate the new cube
                Solver.perform_move(rubiks_cube, key)
                # If the new cube is solved, pick it
                if rubiks_cube.is_solved():
                    next_solve_minimum = -1
                    minimum_move = key
                    # Undo the Scramble caused by the move before exiting
                    Solver.perform_move(rubiks_cube, key + 1 if key % 2 == 0 else key - 1)
                    break
                # Get the evaluation from the model to determine if it is a desired result
                prediction = get_categorical_prediction(model, rubiks_cube)
                if prediction < next_solve_minimum:
                    next_solve_minimum = prediction
                    minimum_move = key
                # Undo the Scramble caused by the move before continuing
                Solver.perform_move(rubiks_cube, key + 1 if key % 2 == 0 else key - 1)
            # After picking the best move, perform it on the cube, and save it for the visualizer later
            move_count += 1
            last_move_reverse = minimum_move + 1 if minimum_move % 2 == 0 else minimum_move - 1
            solve_visual_moves.append(minimum_move)
            Solver.perform_move(rubiks_cube, minimum_move)
        # Show the moves with the visualizer and evaluate the result
        print("\n\n\n")
        total_solves += 1
        for move in solve_visual_moves:
            Solver.perform_move(visual_cube, move)
            # time.sleep(0.3)
        if rubiks_cube.is_solved():
            print("AI Solved cube in {} Moves".format(move_count))
            success_solves += 1
        else:
            print("AI Failed to solve cube in {} Moves".format(MAX_MOVES))
        print("AI Solved Cube {} out of {} times.".format(success_solves, total_solves))
        # time.sleep(1)
