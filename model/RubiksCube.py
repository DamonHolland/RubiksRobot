import copy
import random

SOLVED_CUBE = [(0, 0, 0, 0, 0, 1), (0, 0, 0, 0, 0, 1), (0, 0, 0, 0, 0, 1), (0, 0, 0, 0, 0, 1), (0, 0, 0, 0, 0, 1),
               (0, 0, 0, 0, 0, 1), (0, 0, 0, 0, 0, 1), (0, 0, 0, 0, 0, 1), (0, 0, 0, 0, 0, 1), (0, 0, 0, 0, 1, 0),
               (0, 0, 0, 0, 1, 0), (0, 0, 0, 0, 1, 0), (0, 0, 0, 0, 1, 0), (0, 0, 0, 0, 1, 0), (0, 0, 0, 0, 1, 0),
               (0, 0, 0, 0, 1, 0), (0, 0, 0, 0, 1, 0), (0, 0, 0, 0, 1, 0), (0, 0, 0, 1, 0, 0), (0, 0, 0, 1, 0, 0),
               (0, 0, 0, 1, 0, 0), (0, 0, 0, 1, 0, 0), (0, 0, 0, 1, 0, 0), (0, 0, 0, 1, 0, 0), (0, 0, 0, 1, 0, 0),
               (0, 0, 0, 1, 0, 0), (0, 0, 0, 1, 0, 0), (0, 0, 1, 0, 0, 0), (0, 0, 1, 0, 0, 0), (0, 0, 1, 0, 0, 0),
               (0, 0, 1, 0, 0, 0), (0, 0, 1, 0, 0, 0), (0, 0, 1, 0, 0, 0), (0, 0, 1, 0, 0, 0), (0, 0, 1, 0, 0, 0),
               (0, 0, 1, 0, 0, 0), (0, 1, 0, 0, 0, 0), (0, 1, 0, 0, 0, 0), (0, 1, 0, 0, 0, 0), (0, 1, 0, 0, 0, 0),
               (0, 1, 0, 0, 0, 0), (0, 1, 0, 0, 0, 0), (0, 1, 0, 0, 0, 0), (0, 1, 0, 0, 0, 0), (0, 1, 0, 0, 0, 0),
               (1, 0, 0, 0, 0, 0), (1, 0, 0, 0, 0, 0), (1, 0, 0, 0, 0, 0), (1, 0, 0, 0, 0, 0), (1, 0, 0, 0, 0, 0),
               (1, 0, 0, 0, 0, 0), (1, 0, 0, 0, 0, 0), (1, 0, 0, 0, 0, 0), (1, 0, 0, 0, 0, 0)]


class RubiksCube:
    WHITE = (0, 0, 0, 0, 0, 1)
    GREEN = (0, 0, 0, 0, 1, 0)
    RED = (0, 0, 0, 1, 0, 0)
    BLUE = (0, 0, 1, 0, 0, 0)
    ORANGE = (0, 1, 0, 0, 0, 0)
    YELLOW = (1, 0, 0, 0, 0, 0)
    CUBE_FACES = [WHITE, GREEN, RED, BLUE, ORANGE, YELLOW]
    PIECE_FACES_PER_SIDE = 9

    HUMAN_READABLE = {WHITE: 'W',
                      GREEN: 'G',
                      RED: 'R',
                      BLUE: 'B',
                      ORANGE: 'O',
                      YELLOW: 'Y'}

    def __init__(self, faces=None):
        self.verbose = False
        self.faces = []
        self.last_move = -1
        self.last_move2 = -1
        if not faces: self.faces = SOLVED_CUBE
        else: self.faces = faces

    def reset(self):
        self.verbose = False
        self.faces = SOLVED_CUBE
        self.last_move = -1
        self.last_move2 = -1

    def as_string(self):
        string = ""
        for face in self.faces:
            string += self.HUMAN_READABLE[face]
        return string

    def scramble(self, move_count):
        if self.verbose:
            print("Scrambling Cube {} turns".format(str(move_count)))
        possible_moves = [lambda cc: self.rotate_white(cc), lambda cc: self.rotate_green(cc),
                          lambda cc: self.rotate_red(cc), lambda cc: self.rotate_blue(cc),
                          lambda cc: self.rotate_orange(cc), lambda cc: self.rotate_yellow(cc)]
        scramble_moves = []
        encountered_states = []
        next_move = 0
        for i in range(move_count):
            # record current state, and save it as an encountered state
            previous_state = next_state = copy.copy(self.faces)
            encountered_states.append(previous_state)
            while encountered_states.count(next_state) > 0:
                # Revert cube to previous state
                self.faces = copy.copy(previous_state)
                # Apply a random move, don't allow same move 3 in a row
                next_move = random.randint(0, 11)
                while next_move == self.last_move and next_move == self.last_move2:
                    next_move = random.randint(0, 11)
                possible_moves[int(next_move / 2)](next_move % 2)
                next_state = copy.copy(self.faces)
            scramble_moves.append(next_move)
            self.last_move2 = self.last_move
            self.last_move = next_move
        return scramble_moves

    def rotate_white(self, cc=False):
        if self.verbose: print("Rotating White {}".format("CounterClockwise (U')" if cc else "Clockwise (U)"))
        self._rotate_swap(1, 5, 7, 3, cc)
        self._rotate_swap(0, 2, 8, 6, cc)
        self._rotate_swap(9, 36, 27, 18, cc)
        self._rotate_swap(10, 37, 28, 19, cc)
        self._rotate_swap(11, 38, 29, 20, cc)

    def rotate_green(self, cc=False):
        if self.verbose: print("Rotating Green {}".format("CounterClockwise (F')" if cc else "Clockwise (F)"))
        self._rotate_swap(10, 14, 16, 12, cc)
        self._rotate_swap(9, 11, 17, 15, cc)
        self._rotate_swap(8, 24, 47, 38, cc)
        self._rotate_swap(7, 21, 50, 41, cc)
        self._rotate_swap(6, 18, 53, 44, cc)

    def rotate_red(self, cc=False):
        if self.verbose: print("Rotating Red {}".format("CounterClockwise (R')" if cc else "Clockwise (R)"))
        self._rotate_swap(19, 23, 25, 21, cc)
        self._rotate_swap(18, 20, 26, 24, cc)
        self._rotate_swap(2, 33, 53, 11, cc)
        self._rotate_swap(5, 30, 52, 14, cc)
        self._rotate_swap(8, 27, 51, 17, cc)

    def rotate_blue(self, cc=False):
        if self.verbose: print("Rotating Blue {}".format("CounterClockwise (B')" if cc else "Clockwise (B)"))
        self._rotate_swap(28, 32, 34, 30, cc)
        self._rotate_swap(27, 29, 35, 33, cc)
        self._rotate_swap(0, 42, 51, 20, cc)
        self._rotate_swap(1, 39, 48, 23, cc)
        self._rotate_swap(2, 36, 45, 26, cc)

    def rotate_orange(self, cc=False):
        if self.verbose: print("Rotating Orange {}".format("CounterClockwise (L')" if cc else "Clockwise (L)"))
        self._rotate_swap(37, 41, 43, 39, cc)
        self._rotate_swap(36, 38, 44, 42, cc)
        self._rotate_swap(6, 15, 45, 29, cc)
        self._rotate_swap(3, 12, 46, 32, cc)
        self._rotate_swap(0, 9, 47, 35, cc)

    def rotate_yellow(self, cc=False):
        if self.verbose: print("Rotating Yellow {}".format("CounterClockwise (D')" if cc else "Clockwise (D)"))
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

    def is_solved(self):
        return self.faces == SOLVED_CUBE
