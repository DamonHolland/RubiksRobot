from RubiksVisualizer import RubiksVisualizer
from RubiksCube import RubiksCube


if __name__ == '__main__':
    rubiks_cube = RubiksCube()
    rubiks_cube.rotateWhiteC()
    rubiks_cube.rotateWhiteCC()
    visuals = RubiksVisualizer(rubiks_cube)
