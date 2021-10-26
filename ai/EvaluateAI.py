import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import ai.RubiksDataset as Data
from ai.RubiksMoves import MoveDecoder, perform_move
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
SOLVED_VALUE = 1000
MAX_NODES = 10000


def get_categorical_prediction(cube) -> int:
    # Gets the numerical prediction from the neural network
    # This value is the estimated number of solves left
    predictions = model(np.array([Data.encode_to_input(cube)]))[0]
    return np.argmax(predictions, axis=0) + 1


class Node:
    depth: int
    move_list: list
    value: int

    def __init__(self, depth: int, move_list: list, initial_cube: RubiksCube):
        # Depth of this node and the move list to get to this configuration
        self.move_list = move_list
        self.depth = depth
        value_cube = RubiksCube()
        value_cube.faces = copy.copy(initial_cube.faces)
        for attempt_move in self.move_list:
            perform_move(value_cube, attempt_move)
        if value_cube.is_solved():
            self.value = SOLVED_VALUE
        else:
            self.value = get_categorical_prediction(value_cube) + self.depth


if __name__ == '__main__':
    print("\nEvaluating Model\n")
    total_solves = 0
    success_solves = 0
    rubiks_cube = RubiksCube()
    RubiksVisualizer(rubiks_cube)
    # Evaluates until you exit the program
    while True:
        counter = itertools.count()
        last_move_reverse = -1
        rubiks_cube.reset()
        rubiks_cube.scramble(NUM_SCRAMBLES)
        print("Cube scrambled {} times".format(NUM_SCRAMBLES))

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
                visited_nodes += 1
                new_node = Node(popped_node.depth + 1, popped_node.move_list + [move], rubiks_cube)
                # If the new node is a solved node, exit
                if new_node.value == SOLVED_VALUE:
                    found_solution_node = new_node
                    break
                pq.put((new_node.value, next(counter), new_node))
        print("Visited Nodes: {}".format(visited_nodes))
        total_solves += 1
        # Evaluate the result
        if found_solution_node:
            print("AI Solved cube in {} Moves".format(len(found_solution_node.move_list)))
            success_solves += 1
            # Show the moves with the visualizer
            time.sleep(1.0)
            for move in found_solution_node.move_list:
                perform_move(rubiks_cube, move)
                time.sleep(0.5)
            time.sleep(1.0)
        else:
            print("AI Failed to solve cube in within {} nodes".format(MAX_NODES))
        print("AI Solved Cube {} out of {} times. ({}%)\n".format(success_solves, total_solves, (success_solves / total_solves) * 100))
