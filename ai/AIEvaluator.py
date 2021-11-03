import random
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ai.RubiksMoves import encode_to_input
import tensorflow as tf
import numpy as np
from RubiksDataset import RubiksDatabase


class AISolver:
    def __init__(self, model_name):
        self.model = tf.keras.models.load_model("models/" + model_name)

    def get_categorical_prediction(self, state) -> int:
        return np.argmax(self.model(np.array([state]))[0], axis=0) + 1


if __name__ == '__main__':
    SCRAMBLES = 8
    ai_solver = AISolver("8_Training")
    db = RubiksDatabase("RubiksData.db")
    wrong = 0
    total = 0
    while True:
        total += 1
        state, scramble = db.get_data(SCRAMBLES, 9)
        state = state[0]
        scramble = scramble[0] + 1
        ai_guess = ai_solver.get_categorical_prediction(state)
        if ai_guess != scramble:
            wrong += 1
            print("AI Guessed Wrong {}, Correct is {}".format(ai_guess, scramble))
            predictions = ai_solver.model(np.array([state]))[0]
            weighted_sum = 0
            for i in range(len(predictions)):
                weighted_sum += (1 + i) * float(predictions[i])
            print("AI Average is {}".format(weighted_sum))
        print("Correct {} out of {} - {}%".format(total - wrong, total, 100 * (total - wrong) / total))

