import random

class RubiksCube:
    WHITE = (0, 0, 0)
    GREEN = (0, 0, 1)
    RED = (0, 1, 0)
    BLUE = (0, 1, 1)
    ORANGE = (1, 0, 0)
    YELLOW = (1, 0, 1)
    CUBE_FACES = [WHITE, GREEN, RED, BLUE, ORANGE, YELLOW]
    PIECE_FACES_PER_SIDE = 9

    HUMAN_READABLE = { WHITE: 'W',
                       GREEN: 'G',
                       RED: 'R',
                       BLUE: 'B',
                       ORANGE: 'O',
                       YELLOW: 'Y'}

    def __init__(self):
        self.verbose = False
        self.faces = []
        self.last_move = 0
        for face in self.CUBE_FACES:
            for i in range(self.PIECE_FACES_PER_SIDE):
                self.faces.append(face)

    def as_string(self):
        string = ""
        for face in self.faces[0:9]:
            string += self.HUMAN_READABLE[face]
        for face in self.faces[18:27]:
            string += self.HUMAN_READABLE[face]
        for face in self.faces[9:18]:
            string += self.HUMAN_READABLE[face]
        string += self.HUMAN_READABLE[self.faces[47]]
        string += self.HUMAN_READABLE[self.faces[50]]
        string += self.HUMAN_READABLE[self.faces[53]]
        string += self.HUMAN_READABLE[self.faces[46]]
        string += self.HUMAN_READABLE[self.faces[49]]
        string += self.HUMAN_READABLE[self.faces[52]]
        string += self.HUMAN_READABLE[self.faces[45]]
        string += self.HUMAN_READABLE[self.faces[48]]
        string += self.HUMAN_READABLE[self.faces[51]]
        for face in self.faces[36:45]:
            string += self.HUMAN_READABLE[face]
        for face in self.faces[27:36]:
            string += self.HUMAN_READABLE[face]
        return string

    def scramble(self, move_count):
        if self.verbose:
            print("Scrambling Cube {} turns".format(str(move_count)))
        possible_moves = [lambda cc: self.rotate_white(cc), lambda cc: self.rotate_green(cc), lambda cc: self.rotate_red(cc),
                          lambda cc: self.rotate_blue(cc), lambda cc: self.rotate_orange(cc), lambda cc: self.rotate_yellow(cc)]
        for i in range(move_count):
            self.last_move = random.randint(0, 11)
            possible_moves[int(self.last_move / 2)](self.last_move % 2)

    def rotate_white(self, cc=False):
        if self.verbose:
            print("Rotating White {}".format("CounterClockwise (U')" if cc else "Clockwise (U)"))
        self._rotate_swap(1, 5, 7, 3, cc)
        self._rotate_swap(0, 2, 8, 6, cc)
        self._rotate_swap(9, 36, 27, 18, cc)
        self._rotate_swap(10, 37, 28, 19, cc)
        self._rotate_swap(11, 38, 29, 20, cc)

    def rotate_green(self, cc=False):
        if self.verbose:
            print("Rotating Green {}".format("CounterClockwise (F')" if cc else "Clockwise (F)"))
        self._rotate_swap(10, 14, 16, 12, cc)
        self._rotate_swap(9, 11, 17, 15, cc)
        self._rotate_swap(8, 24, 47, 38, cc)
        self._rotate_swap(7, 21, 50, 41, cc)
        self._rotate_swap(6, 18, 53, 44, cc)

    def rotate_red(self, cc=False):
        if self.verbose:
            print("Rotating Red {}".format("CounterClockwise (R')" if cc else "Clockwise (R)"))
        self._rotate_swap(19, 23, 25, 21, cc)
        self._rotate_swap(18, 20, 26, 24, cc)
        self._rotate_swap(2, 33, 53, 11, cc)
        self._rotate_swap(5, 30, 52, 14, cc)
        self._rotate_swap(8, 27, 51, 17, cc)

    def rotate_blue(self, cc=False):
        if self.verbose:
            print("Rotating Blue {}".format("CounterClockwise (B')" if cc else "Clockwise (B)"))
        self._rotate_swap(28, 32, 34, 30, cc)
        self._rotate_swap(27, 29, 35, 33, cc)
        self._rotate_swap(0, 42, 51, 20, cc)
        self._rotate_swap(1, 39, 48, 23, cc)
        self._rotate_swap(2, 36, 45, 26, cc)

    def rotate_orange(self, cc=False):
        if self.verbose:
            print("Rotating Orange {}".format("CounterClockwise (L')" if cc else "Clockwise (L)"))
        self._rotate_swap(37, 41, 43, 39, cc)
        self._rotate_swap(36, 38, 44, 42, cc)
        self._rotate_swap(6, 15, 45, 29, cc)
        self._rotate_swap(3, 12, 46, 32, cc)
        self._rotate_swap(0, 9, 47, 35, cc)

    def rotate_yellow(self, cc=False):
        if self.verbose:
            print("Rotating Yellow {}".format("CounterClockwise (D')" if cc else "Clockwise (D)"))
        self._rotate_swap(46, 50, 52, 48, cc)
        self._rotate_swap(45, 47, 53, 51, cc)
        self._rotate_swap(17, 26, 35, 44, cc)
        self._rotate_swap(16, 25, 34, 43, cc)
        self._rotate_swap(15, 24, 33, 42, cc)

    def _rotate_swap(self, index_1, index_2, index_3, index_4, cc=False):
        self.faces[index_1], self.faces[index_2], self.faces[index_3], self.faces[index_4] = \
            (self.faces[index_2], self.faces[index_3], self.faces[index_4], self.faces[index_1]) if cc \
                else (self.faces[index_4], self.faces[index_1], self.faces[index_2], self.faces[index_3])

    def enable_logging(self):
        self.verbose = True

    def disable_logging(self):
        self.verbose = False

