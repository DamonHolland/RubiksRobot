
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
        for face in self.CUBE_FACES:
            for i in range(self.PIECE_FACES_PER_SIDE):
                self.faces += face
        print("Rubik's Cube Initialized with colors: {}".format(self.asString()))

    def asString(self):
        string = ""
        index = 0
        for face in self.faces:
            string += face
            index += 1
            if index % 9 == 0:
                string += ' '
        return string

    def rotateWhiteC(self):
        print("Rotating white face clockwise (U)")
        # FACE:
        self._swap(0, 2, 8, 6)
        self._swap(1, 5, 3, 7)
        # BORDER:
        self._swap(10, 37, 28, 19)
        self._swap(9, 36, 27, 18)
        self._swap(11, 38, 29, 20)
        print("New Orientation: {}".format(self.asString()))

    def rotateWhiteCC(self):
        print("Rotating white face clockwise (U')")
        # FACE:
        self._swap(0, 2, 8, 6, cc=True)
        self._swap(1, 5, 3, 7, cc=True)
        # BORDER:
        self._swap(10, 37, 28, 19, cc=True)
        self._swap(9, 36, 27, 18, cc=True)
        self._swap(11, 38, 29, 20, cc=True)
        print("New Orientation: {}".format(self.asString()))

    def rotateGreenC(self):
        print("Rotating green face clockwise (F)")
        # FACE:
        # 11 -> 15 -> 17 -> 13
        # 1 -> 5 -> 3 -> 7
        # BORDER:
        # 10 -> 37 -> 28 -> 19
        # 9 -> 36 -> 27 -> 18
        # 11 -> 38 -> 29 -> 20

    def _swap(self, index_1, index_2, index_3, index_4, cc=False):
        if cc:
            temp = self.faces[index_1]
            self.faces[index_1] = self.faces[index_2]
            self.faces[index_2] = self.faces[index_3]
            self.faces[index_3] = self.faces[index_4]
            self.faces[index_4] = temp
        else:
            temp = self.faces[index_1]
            self.faces[index_1] = self.faces[index_4]
            self.faces[index_4] = self.faces[index_3]
            self.faces[index_3] = self.faces[index_2]
            self.faces[index_2] = temp
