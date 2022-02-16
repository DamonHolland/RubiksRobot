import sys
import os.path
import time

from model.RubiksCube import RubiksCube

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from RubiksDataset import RubiksDatabase
from AISolver import AISolver


def cube_from_encoding(encoding):
    new_cube = RubiksCube()
    faces = []
    for face in encoding:
        faces.append(face)
    new_cube.faces = faces
    print(len(new_cube.faces))
    return new_cube


if __name__ == '__main__':
    SCRAMBLES = 9
    ai_solver = AISolver("models/9_Training")
    db = RubiksDatabase()
    wrong = 0
    total = 0
    cube = RubiksCube()
    while True:
        total += 1
        state, scramble = db.get_data(SCRAMBLES, 9)
        state = state[0]
        scramble = scramble[0] + 1
        ai_guess = ai_solver.model.predict_single(state)
        weighted_sum = 0
        for i in range(len(ai_guess)):
            weighted_sum += (1 + i) * float(ai_guess[i])
        ai_guess = weighted_sum // 1
        if ai_guess != scramble:
            wrong += 1
            print("AI Guessed Wrong {}, Correct is {}".format(ai_guess, scramble))
        print("Correct {} out of {} - {}%".format(total - wrong, total, 100 * (total - wrong) / total))
