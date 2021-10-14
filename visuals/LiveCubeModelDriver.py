import time
from visuals.RubiksVisualizer import RubiksVisualizer
from model.RubiksCube import RubiksCube


def scramble_speed_test():
    rubiks_cube = RubiksCube()
    num_scrambles = 0
    scramble_move_count = 30
    t_end = time.time() + 1
    while time.time() < t_end:
        rubiks_cube.scramble(scramble_move_count)
        num_scrambles += 1
    print("\n\nPerformed {} {} move scrambles in 1 second.".format(num_scrambles, scramble_move_count))


def visualizer_test():
    rubiks_cube = RubiksCube()
    rubiks_cube.enable_logging()
    RubiksVisualizer(rubiks_cube)
    time.sleep(5)
    for i in range(30):
        time.sleep(0.5)
        rubiks_cube.scramble(1)


if __name__ == '__main__':
    scramble_speed_test()
    # visualizer_test()
