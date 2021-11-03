import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from visuals.RubiksVisualizer import RubiksVisualizer
from ai.RubiksMoves import MoveDecoder, perform_move, move_reverse, encode_to_input
from model.RubiksCube import RubiksCube
import tensorflow as tf
import numpy as np
import copy
import time
import itertools
from queue import PriorityQueue


class Node:
    move_list: list
    value: float

    def __init__(self, move_list: list, initial_cube: RubiksCube, predictor):
        self.move_list = move_list
        value_cube = RubiksCube()
        value_cube.faces = copy.copy(initial_cube.faces)
        for attempt_move in self.move_list:
            perform_move(value_cube, attempt_move)
        self.value = sys.maxsize if value_cube.is_solved() else predictor(value_cube) + len(self.move_list) * 1.1


class AISolver:
    def __init__(self, model_name):
        self.model = tf.keras.models.load_model("models/" + model_name)
        self.counter = itertools.count()

    def solve(self, cube, time_limit):
        pq = PriorityQueue()
        first_node = Node([], cube, self.get_categorical_prediction)
        pq.put((first_node.value, next(self.counter), first_node))
        found_solution_node = None
        start_time = time.time()
        while not found_solution_node and time.time() - start_time <= time_limit:
            popped_node: Node = pq.get()[2]
            for move in MoveDecoder.keys():
                if len(popped_node.move_list) != 0:
                    if move == move_reverse(popped_node.move_list[len(popped_node.move_list) - 1]):
                        continue
                new_node = Node(popped_node.move_list + [move], cube, self.get_categorical_prediction)
                if new_node.value == sys.maxsize:
                    found_solution_node = new_node
                    break
                pq.put((new_node.value, next(self.counter), new_node))
        return found_solution_node.move_list if found_solution_node else None

    def get_categorical_prediction(self, cube) -> int:
        predictions = self.model(np.array([encode_to_input(cube)]))[0]
        weighted_sum = 0
        for i in range(len(predictions)):
            weighted_sum += (1 + i) * float(predictions[i])
        return weighted_sum


if __name__ == '__main__':
    SCRAMBLE_AMOUNT = 9
    TIME_LIMIT = 10
    ai_solver = AISolver("8_Training")
    rubiks_cube = RubiksCube()
    visualizer = RubiksVisualizer(rubiks_cube)
    total = 0
    success = 0
    while True:
        # time.sleep(1.0)
        rubiks_cube.reset()
        start_t = time.time()
        print("Scrambled cube {} moves.".format(SCRAMBLE_AMOUNT))
        rubiks_cube.scramble(SCRAMBLE_AMOUNT)
        solve_moves = ai_solver.solve(rubiks_cube, TIME_LIMIT)
        if solve_moves:
            success += 1
            print("AI solved cube in {} moves.".format(len(solve_moves)))
            print("AI solved cube in {} seconds.".format(round(time.time() - start_t, 2)))
            for solve_move in solve_moves:
                # time.sleep(0.5)
                perform_move(rubiks_cube, solve_move)
        else:
            print("AI failed to solve cube in {} seconds".format(TIME_LIMIT))
        total += 1
        print("Cube solved {} out of {} times ({}%).\n\n".format(success, total, 100 * success / total))
