from RubiksVisualizer import RubiksVisualizer
from RubiksCube import RubiksCube


if __name__ == '__main__':
    rubiks_cube = RubiksCube()
    rubiks_cube.shuffle(15)
    visuals = RubiksVisualizer(rubiks_cube)
