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
import time
import itertools
from queue import PriorityQueue

# Evaluation Config
NUM_SCRAMBLES = 5
# Load Model
MODEL_NAME = "5_Perfect"
model = tf.keras.models.load_model("models/" + MODEL_NAME)
CUBE_SOLVED = 1000
MAX_NODES = 3000


def get_categorical_prediction(cube) -> int:
    # Gets the numerical prediction from the neural network
    # This value is the estimated number of solves left
    predictions = model(np.array([Data.encode_to_input(cube)]))[0]
    return np.argmax(predictions, axis=0) + 1


class Node:
    depth: int
    move_list: list
    value = 0

    def __init__(self, depth: int, move_list: list, initial_cube: RubiksCube):
        # Depth of this node and the move list to get to this configuration
        self.move_list = move_list
        self.depth = depth
        value_cube = RubiksCube()
        value_cube.faces = copy.copy(initial_cube.faces)
        for attempt_move in self.move_list:
            Solver.perform_move(value_cube, attempt_move)
        if value_cube.is_solved():
            self.value = CUBE_SOLVED
        else:
            self.value = get_categorical_prediction(value_cube) + (self.depth * 1.2)


if __name__ == '__main__':
    print("\nEvaluating Model\n")
    total_solves = 0
    success_solves = 0
    visual_cube = RubiksCube()
    RubiksVisualizer(visual_cube)
    # Evaluates until you exit the program
    while True:
        counter = itertools.count()
        solve_visual_moves = []
        last_move_reverse = -1
        rubiks_cube = RubiksCube()
        rubiks_cube.scramble(NUM_SCRAMBLES)
        visual_cube.faces = copy.copy(rubiks_cube.faces)

        pq = PriorityQueue()
        # Add first node to priority queue
        first_node = Node(0, [], rubiks_cube)
        pq.put((first_node.value, next(counter), first_node))
        # Pop off Nodes Until a solution is found
        found_solution_node = None
        visited_nodes = 0
        while not found_solution_node and visited_nodes < MAX_NODES:
            # Pop highest priority node off of the queue
            popped_node: Node = pq.get()[2]
            for move in MoveDecoder.keys():
                # Add all children of the highest priority node to the priority queue
                new_node = Node(popped_node.depth + 1, popped_node.move_list + [move], rubiks_cube)
                visited_nodes += 1
                # If the new node is a solved node, exit
                if new_node.value == CUBE_SOLVED:
                    found_solution_node = new_node
                    break
                pq.put((new_node.value, next(counter), new_node))
        print("Visited Nodes: {}".format(visited_nodes))
        total_solves += 1
        # Evaluate the result
        if found_solution_node:
            solution = found_solution_node.move_list
            print("AI Solved cube in {} Moves".format(len(solution)))
            success_solves += 1
            # Show the moves with the visualizer
            for move in solution:
                Solver.perform_move(visual_cube, move)
                # time.sleep(0.5)
        else:
            print("AI Failed to solve cube in within {} nodes".format(MAX_NODES))

        print("AI Solved Cube {} out of {} times.\n".format(success_solves, total_solves))
        # time.sleep(0.5)
