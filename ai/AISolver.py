import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from visuals.RubiksVisualizer import RubiksVisualizer
from ai.RubiksMoves import MoveDecoder, perform_move, move_reverse, encode_to_input
from model.RubiksCube import RubiksCube
import tensorflow as tf
import copy
import time
import itertools
from queue import PriorityQueue
from ai.LiteModel import LiteModel
from ai.KociembaSolver import KociembaSolver


class Node:
    moves: list
    value: float

    def __init__(self, moves: list, initial_cube: RubiksCube, predictor):
        self.moves = moves
        value_cube = RubiksCube()
        value_cube.faces = copy.copy(initial_cube.faces)
        for attempt_move in self.moves:
            perform_move(value_cube, attempt_move)
        self.value = -sys.maxsize if value_cube.is_solved() else predictor(value_cube) + len(self.moves)


class AISolver:
    def __init__(self, model_dir):
        self.model = tf.keras.models.load_model(model_dir)
        self.model = LiteModel.from_keras_model(self.model)
        self.counter = itertools.count()

    def solve(self, cube, time_limit):
        pq = PriorityQueue()
        first_node = Node([], cube, self.get_categorical_prediction)
        pq.put((first_node.value, next(self.counter), first_node))
        start_time = time.time()
        solution_node = None
        while time.time() - start_time <= time_limit and not solution_node:
            p_node: Node = pq.get()[2]
            for move in MoveDecoder.keys():
                last_move = p_node.moves[len(p_node.moves) - 1] if len(p_node.moves) != 0 else None
                if last_move and move == move_reverse(last_move):
                    continue
                new_node = Node(p_node.moves + [move], cube, self.get_categorical_prediction)
                if new_node.value == -sys.maxsize:
                    solution_node = new_node
                    break
                else:
                    pq.put((new_node.value, next(self.counter), new_node))
        if not solution_node:
            k_solver = KociembaSolver()
            print("AI did not find solution. Kociembas algorithm was used as backup.")
            return k_solver.solve(cube)
        return solution_node.moves

    def get_categorical_prediction(self, cube) -> int:
        predictions = self.model.predict_single(encode_to_input(cube))
        weighted_sum = 0
        for i in range(len(predictions)):
            weighted_sum += (1 + i) * float(predictions[i])
        return weighted_sum


if __name__ == '__main__':
    SCRAMBLE_AMOUNT = 10
    TIME_LIMIT = 10
    ai_solver = AISolver("models/9_Training")
    rubiks_cube = RubiksCube()
    visualizer = RubiksVisualizer(rubiks_cube)
    total = 0
    success = 0
    while True:
        time.sleep(1.0)
        rubiks_cube.reset()
        start_t = time.time()
        print("Scrambled cube {} moves.".format(SCRAMBLE_AMOUNT))
        rubiks_cube.scramble(SCRAMBLE_AMOUNT)
        solve_moves = ai_solver.solve(rubiks_cube, TIME_LIMIT)
        if solve_moves:
            solve_parsed = []
            for move in solve_moves:
                solve_parsed.append(MoveDecoder[move])
            print(solve_parsed)
            success += 1
            print("AI solved cube in {} moves.".format(len(solve_moves)))
            print("AI solved cube in {} seconds.".format(round(time.time() - start_t, 2)))
            for solve_move in solve_moves:
                time.sleep(0.5)
                perform_move(rubiks_cube, solve_move)
        else:

            print("AI failed to solve cube in {} seconds".format(TIME_LIMIT))
        total += 1
        print("Cube solved {} out of {} times ({}%).\n\n".format(success, total, 100 * success / total))
