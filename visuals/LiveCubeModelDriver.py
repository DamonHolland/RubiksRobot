import time

from visuals.RubiksVisualizer import RubiksVisualizer
from model.RubiksCube import RubiksCube
from threading import Thread


def shuffleCube(cube):
    for i in range(50):
        time.sleep(0.3)
        cube.shuffle(1)


if __name__ == '__main__':
    rubiks_cube = RubiksCube()
    visuals = RubiksVisualizer()
    visual_thread = Thread(target=visuals.start, args=[rubiks_cube])
    visual_thread.start()
    shuffle_thread = Thread(target=shuffleCube, args=[rubiks_cube])
    shuffle_thread.start()

