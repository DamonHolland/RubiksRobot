from threading import Thread

from model.RubiksCube import RubiksCube
from visuals.RubiksVisualizer import RubiksVisualizer

if __name__ == '__main__':
    rubiks_cube = RubiksCube()
    visuals = RubiksVisualizer()
    visual_thread = Thread(target=visuals.start, args=[rubiks_cube])
    visual_thread.start()


