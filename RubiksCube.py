
class RubiksCube:
    WHITE = 'W'
    GREEN = 'G'
    RED = 'R'
    BLUE = 'B'
    ORANGE = 'O'
    YELLOW = 'Y'
    CUBE_FACES = [WHITE, GREEN, RED, BLUE, ORANGE, YELLOW]
    PIECE_FACES_PER_SIDE = 9

    def __init__(self):
        self.faces = ""
        for face in self.CUBE_FACES:
            for i in range(self.PIECE_FACES_PER_SIDE):
                self.faces += face
        print("Rubik's Cube Initialized with colors: {}".format(self.faces))
