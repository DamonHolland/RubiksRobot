import random

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
        self.faces = []
        self.last_move = 0
        for face in self.CUBE_FACES:
                self.faces += face * self.PIECE_FACES_PER_SIDE

    def asString(self):
        string = ""
        for i in range(len(self.faces)):
            string += (' ' if i % 9 == 0 else '') + self.faces[i]
        return string

    def scramble(self, move_count):
        if move_count <= 0:
            raise Exception
        possible_moves = [lambda cc: self.rotateWhite(cc), lambda cc: self.rotateGreen(cc), lambda cc: self.rotateRed(cc),
                          lambda cc: self.rotateBlue(cc), lambda cc: self.rotateOrange(cc), lambda cc: self.rotateYellow(cc)]
        for i in range(move_count):
            self.last_move = random.randint(0, 11)
            possible_moves[int(self.last_move / 2)](self.last_move % 2)

    def rotateWhite(self, cc=False):
        self._rotate_swap(1, 5, 7, 3, cc)
        self._rotate_swap(0, 2, 8, 6, cc)
        self._rotate_swap(9, 36, 27, 18, cc)
        self._rotate_swap(10, 37, 28, 19, cc)
        self._rotate_swap(11, 38, 29, 20, cc)

    def rotateGreen(self, cc=False):
        self._rotate_swap(10, 14, 16, 12, cc)
        self._rotate_swap(9, 11, 17, 15, cc)
        self._rotate_swap(8, 24, 47, 38, cc)
        self._rotate_swap(7, 21, 50, 41, cc)
        self._rotate_swap(6, 18, 53, 44, cc)

    def rotateRed(self, cc=False):
        self._rotate_swap(19, 23, 25, 21, cc)
        self._rotate_swap(18, 20, 26, 24, cc)
        self._rotate_swap(2, 33, 53, 11, cc)
        self._rotate_swap(5, 30, 52, 14, cc)
        self._rotate_swap(8, 27, 51, 17, cc)

    def rotateBlue(self, cc=False):
        self._rotate_swap(28, 32, 34, 30, cc)
        self._rotate_swap(27, 29, 35, 33, cc)
        self._rotate_swap(0, 42, 51, 20, cc)
        self._rotate_swap(1, 39, 48, 23, cc)
        self._rotate_swap(2, 36, 45, 26, cc)

    def rotateOrange(self, cc=False):
        self._rotate_swap(37, 41, 43, 39, cc)
        self._rotate_swap(36, 38, 44, 42, cc)
        self._rotate_swap(6, 15, 45, 29, cc)
        self._rotate_swap(3, 12, 46, 32, cc)
        self._rotate_swap(0, 9, 47, 35, cc)

    def rotateYellow(self, cc=False):
        self._rotate_swap(46, 50, 52, 48, cc)
        self._rotate_swap(45, 47, 53, 51, cc)
        self._rotate_swap(17, 26, 35, 44, cc)
        self._rotate_swap(16, 25, 34, 43, cc)
        self._rotate_swap(15, 24, 33, 42, cc)

    def _rotate_swap(self, index_1, index_2, index_3, index_4, cc=False):
        self.faces[index_1], self.faces[index_2], self.faces[index_3], self.faces[index_4] = \
            (self.faces[index_2], self.faces[index_3], self.faces[index_4], self.faces[index_1]) if cc \
                else (self.faces[index_4], self.faces[index_1], self.faces[index_2], self.faces[index_3])

