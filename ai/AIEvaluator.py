import sys
import os.path

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
    SCRAMBLES = 10
    SAMPLE_SIZE = 1000
    ai_solver = AISolver("models/10_Model")
    db = RubiksDatabase()
    wrong = 0
    total = 0
    cube = RubiksCube()
    stateData, scrambleData = db.get_data(SCRAMBLES, SAMPLE_SIZE)
    for i in range(len(scrambleData)):
        total += 1
        state = stateData[i]
        scramble = scrambleData[i] + 1
        ai_guess = list(ai_solver.model.predict_single(state))
        ai_guess = ai_guess.index(max(ai_guess)) + 1
        if ai_guess != scramble:
            wrong += 1
            print("AI Guessed Wrong {}, Correct is {}".format(ai_guess, scramble))
        print("Correct {} out of {} - {}%".format(total - wrong, total, 100 * (total - wrong) / total))
