import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from visuals.RubiksVisualizer import RubiksVisualizer
from ai.RubiksMoves import MoveDecoder, perform_move, encode_to_input
from model.RubiksCube import RubiksCube
import tensorflow as tf
import copy
import time
import heapq
from ai.LiteModel import LiteModel
from ai.KociembaSolver import KociembaSolver


class Node:
    def __init__(self, moves: list, cube: RubiksCube, predictor):
        self.moves = moves
        self.depth = len(moves)
        temp_cube = RubiksCube()
        temp_cube.faces = copy.copy(cube.faces)
        [perform_move(temp_cube, m) for m in self.moves]
        self.value = -sys.maxsize if temp_cube.is_solved() else predictor(temp_cube)

    def __lt__(self, other):
        return self.value + self.depth < other.value + other.depth


class AISolver:
    def __init__(self, model_dir):
        self.model = LiteModel.from_keras_model(tf.keras.models.load_model(model_dir))

    def solve(self, cube, time_limit):
        heap = [Node([], cube, self.get_categorical_prediction)]
        heapq.heapify(heap)
        start_time = time.time()
        v = 1
        while time.time() - start_time <= time_limit:
            first: Node = heapq.heappop(heap)
            # print("Starting with node: {}, Depth: {}".format(str(first.value), str(first.depth)))
            for new in [Node(first.moves + [m], cube, self.get_categorical_prediction) for m in MoveDecoder.keys()]:
                # print("Adding node: {}, Depth: {}".format(str(new.value), str(new.depth)))
                if new.value == -sys.maxsize:
                    print("Visited Nodes: {}".format(str(v)))
                    return new.moves
                heapq.heappush(heap, new)
                v += 1
        print("Visited Nodes: {}".format(str(v)))
        print("AI did not find solution. Kociemba algorithm was used as backup.")
        return KociembaSolver().solve(cube)

    def get_categorical_prediction(self, cube) -> int:
        predictions = list(self.model.predict_single(encode_to_input(cube)))
        return predictions.index(max(predictions)) + 1


if __name__ == '__main__':
    SCRAMBLE_AMOUNT = 1000
    TIME_LIMIT = 10
    ai_solver = AISolver("models/Training")
    rubiks_cube = RubiksCube()
    visualizer = RubiksVisualizer(rubiks_cube)
    total, success = 0, 0
    while True:
        time.sleep(1)
        rubiks_cube.reset()
        start_t = time.time()
        print("Scrambled cube {} moves.".format(SCRAMBLE_AMOUNT))
        rubiks_cube.scramble(SCRAMBLE_AMOUNT)
        solve_moves = ai_solver.solve(rubiks_cube, TIME_LIMIT)
        if time.time() - start_t < TIME_LIMIT:
            solve_parsed = [MoveDecoder[move] for move in solve_moves]
            print("AI solved cube in {} moves. {}".format(len(solve_moves), str(solve_parsed)))
            print("AI solved cube in {} seconds.".format(round(time.time() - start_t, 2)))
            for solve_move in solve_moves:
                time.sleep(0.5)
                perform_move(rubiks_cube, solve_move)
            success += 1
        else:
            print("AI failed to solve cube in {} seconds".format(TIME_LIMIT))
            for solve_move in solve_moves:
                time.sleep(0.5)
                perform_move(rubiks_cube, solve_move)
        total += 1
        print("Cube solved {} out of {} times ({}%).\n\n".format(success, total, 100 * success / total))
